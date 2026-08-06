import importlib.util
import inspect
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1] / "imagegen" / "scripts" / "image_gen.py"
)
SPEC = importlib.util.spec_from_file_location("image_gen", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {SCRIPT_PATH}")
image_gen = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = image_gen
SPEC.loader.exec_module(image_gen)


class CredentialResolutionTests(unittest.TestCase):
    def write_auth(self, codex_home: Path, payload: dict) -> None:
        (codex_home / "auth.json").write_text(json.dumps(payload), encoding="utf-8")

    def test_environment_key_takes_precedence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            self.write_auth(
                codex_home,
                {"auth_mode": "apikey", "OPENAI_API_KEY": "sk-file"},
            )
            with mock.patch.dict(
                os.environ,
                {
                    "CODEX_HOME": str(codex_home),
                    "OPENAI_API_KEY": "  sk-env  ",
                },
                clear=True,
            ):
                resolved = image_gen._resolve_openai_client_config()

        self.assertEqual(resolved.api_key, "sk-env")
        self.assertEqual(resolved.api_key_source, "OPENAI_API_KEY")

    def test_reads_api_key_from_codex_auth_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            (codex_home / "config.toml").write_text(
                'cli_auth_credentials_store = "file"\n',
                encoding="utf-8",
            )
            self.write_auth(
                codex_home,
                {"auth_mode": "apikey", "OPENAI_API_KEY": "sk-file"},
            )
            with mock.patch.dict(
                os.environ,
                {"CODEX_HOME": str(codex_home)},
                clear=True,
            ):
                resolved = image_gen._resolve_openai_client_config()

        self.assertEqual(resolved.api_key, "sk-file")
        self.assertIn("auth.json", resolved.api_key_source)

    def test_supports_legacy_auth_json_without_auth_mode(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            self.write_auth(codex_home, {"OPENAI_API_KEY": "sk-legacy"})
            with mock.patch.dict(
                os.environ,
                {"CODEX_HOME": str(codex_home)},
                clear=True,
            ):
                resolved = image_gen._resolve_openai_client_config()

        self.assertEqual(resolved.api_key, "sk-legacy")

    def test_rejects_oauth_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            self.write_auth(
                codex_home,
                {
                    "auth_mode": "chatgpt",
                    "OPENAI_API_KEY": "must-not-be-used",
                    "tokens": {"access_token": "oauth-token"},
                },
            )
            with mock.patch.dict(
                os.environ,
                {"CODEX_HOME": str(codex_home)},
                clear=True,
            ):
                with self.assertRaises(image_gen.CredentialResolutionError) as raised:
                    image_gen._resolve_openai_client_config()

        self.assertIn("not API-key auth", str(raised.exception))

    def test_reads_openai_base_url_from_codex_config(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            (codex_home / "config.toml").write_text(
                "\n".join(
                    [
                        'cli_auth_credentials_store = "file"',
                        'openai_base_url = "https://example.test/v1"',
                    ]
                ),
                encoding="utf-8",
            )
            self.write_auth(codex_home, {"OPENAI_API_KEY": "sk-file"})
            with mock.patch.dict(
                os.environ,
                {"CODEX_HOME": str(codex_home)},
                clear=True,
            ):
                resolved = image_gen._resolve_openai_client_config()

        self.assertEqual(resolved.base_url, "https://example.test/v1")

    def test_environment_base_url_takes_precedence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            (codex_home / "config.toml").write_text(
                'openai_base_url = "https://config.example.test/v1"\n',
                encoding="utf-8",
            )
            self.write_auth(codex_home, {"OPENAI_API_KEY": "sk-file"})
            with mock.patch.dict(
                os.environ,
                {
                    "CODEX_HOME": str(codex_home),
                    "OPENAI_BASE_URL": "https://env.example.test/v1",
                },
                clear=True,
            ):
                resolved = image_gen._resolve_openai_client_config()

        self.assertEqual(resolved.base_url, "https://env.example.test/v1")

    def test_keyring_only_credentials_are_not_extracted(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            (codex_home / "config.toml").write_text(
                'cli_auth_credentials_store = "keyring"\n',
                encoding="utf-8",
            )
            with mock.patch.dict(
                os.environ,
                {"CODEX_HOME": str(codex_home)},
                clear=True,
            ):
                with self.assertRaises(image_gen.CredentialResolutionError) as raised:
                    image_gen._resolve_openai_client_config()

        self.assertIn("OS keyring", str(raised.exception))

    def test_async_client_receives_resolved_configuration(self) -> None:
        captured = {}

        class FakeAsyncOpenAI:
            def __init__(self, **kwargs):
                captured.update(kwargs)

        fake_openai = types.ModuleType("openai")
        fake_openai.AsyncOpenAI = FakeAsyncOpenAI
        resolved = image_gen.OpenAIClientConfig(
            api_key="sk-test",
            api_key_source="test",
            base_url="https://example.test/v1",
        )

        with mock.patch.dict(sys.modules, {"openai": fake_openai}):
            with mock.patch.object(
                image_gen,
                "_resolve_openai_client_config",
                return_value=resolved,
            ):
                client = image_gen._create_async_client()

        self.assertIsInstance(client, FakeAsyncOpenAI)
        self.assertEqual(
            captured,
            {
                "api_key": "sk-test",
                "base_url": "https://example.test/v1",
            },
        )

    def test_all_live_api_commands_are_async(self) -> None:
        self.assertTrue(inspect.iscoroutinefunction(image_gen._generate))
        self.assertTrue(inspect.iscoroutinefunction(image_gen._edit))
        self.assertTrue(inspect.iscoroutinefunction(image_gen._run_generate_batch))


if __name__ == "__main__":
    unittest.main()
