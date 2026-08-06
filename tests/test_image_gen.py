import importlib.util
import inspect
import json
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
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

    def write_config(self, codex_home: Path, contents: str) -> None:
        (codex_home / "config.toml").write_text(contents, encoding="utf-8")

    def test_openai_environment_key_takes_precedence(self) -> None:
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
                resolved = image_gen._resolve_image_api_client_config()

        self.assertEqual(resolved.api_key, "sk-env")
        self.assertEqual(resolved.api_key_source, "OPENAI_API_KEY")
        self.assertEqual(resolved.provider_id, "openai")

    def test_reads_api_key_from_codex_auth_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            self.write_config(codex_home, 'cli_auth_credentials_store = "file"\n')
            self.write_auth(
                codex_home,
                {"auth_mode": "apikey", "OPENAI_API_KEY": "sk-file"},
            )
            with mock.patch.dict(
                os.environ,
                {"CODEX_HOME": str(codex_home)},
                clear=True,
            ):
                resolved = image_gen._resolve_image_api_client_config()

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
                resolved = image_gen._resolve_image_api_client_config()

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
                    image_gen._resolve_image_api_client_config()

        self.assertIn("not API-key auth", str(raised.exception))

    def test_reads_openai_base_url_from_codex_config(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            self.write_config(
                codex_home,
                "\n".join(
                    [
                        'cli_auth_credentials_store = "file"',
                        'openai_base_url = "https://example.test/v1"',
                    ]
                ),
            )
            self.write_auth(codex_home, {"OPENAI_API_KEY": "sk-file"})
            with mock.patch.dict(
                os.environ,
                {"CODEX_HOME": str(codex_home)},
                clear=True,
            ):
                resolved = image_gen._resolve_image_api_client_config()

        self.assertEqual(resolved.base_url, "https://example.test/v1")

    def test_environment_base_url_takes_precedence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            self.write_config(
                codex_home,
                'openai_base_url = "https://config.example.test/v1"\n',
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
                resolved = image_gen._resolve_image_api_client_config()

        self.assertEqual(resolved.base_url, "https://env.example.test/v1")

    def test_keyring_only_credentials_are_not_extracted(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            self.write_config(
                codex_home,
                'cli_auth_credentials_store = "keyring"\n',
            )
            with mock.patch.dict(
                os.environ,
                {"CODEX_HOME": str(codex_home)},
                clear=True,
            ):
                with self.assertRaises(image_gen.CredentialResolutionError) as raised:
                    image_gen._resolve_image_api_client_config()

        self.assertIn("OS keyring", str(raised.exception))

    def test_custom_provider_uses_dynamic_env_key_and_transport_config(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            self.write_config(
                codex_home,
                """
model_provider = "corp"

[model_providers.corp]
name = "Corp Images"
base_url = "https://images.example.test/v1"
env_key = "CORP_IMAGE_API_KEY"
query_params = { region = "us-east" }
http_headers = { "X-Static" = "static-value" }
env_http_headers = { "X-Dynamic" = "CORP_DYNAMIC_HEADER" }
request_max_retries = 7
""",
            )
            with mock.patch.dict(
                os.environ,
                {
                    "CODEX_HOME": str(codex_home),
                    "OPENAI_API_KEY": "must-not-be-used",
                    "CORP_IMAGE_API_KEY": "corp-key",
                    "CORP_DYNAMIC_HEADER": "dynamic-value",
                },
                clear=True,
            ):
                resolved = image_gen._resolve_image_api_client_config()

        self.assertEqual(resolved.provider_id, "corp")
        self.assertEqual(resolved.api_key, "corp-key")
        self.assertEqual(
            resolved.api_key_source,
            "provider environment variable CORP_IMAGE_API_KEY",
        )
        self.assertEqual(resolved.base_url, "https://images.example.test/v1")
        self.assertEqual(
            resolved.default_headers,
            {
                "X-Static": "static-value",
                "X-Dynamic": "dynamic-value",
            },
        )
        self.assertEqual(resolved.default_query, {"region": "us-east"})
        self.assertEqual(resolved.max_retries, 7)

    def test_custom_provider_reports_dynamic_env_key_instructions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            self.write_config(
                codex_home,
                """
model_provider = "corp"

[model_providers.corp]
env_key = "CORP_IMAGE_API_KEY"
env_key_instructions = "Load it from the company password manager."
""",
            )
            with mock.patch.dict(
                os.environ,
                {"CODEX_HOME": str(codex_home)},
                clear=True,
            ):
                with self.assertRaises(image_gen.CredentialResolutionError) as raised:
                    image_gen._resolve_image_api_client_config()

        message = str(raised.exception)
        self.assertIn("CORP_IMAGE_API_KEY", message)
        self.assertIn("company password manager", message)

    def test_custom_provider_supports_experimental_bearer_token(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            self.write_config(
                codex_home,
                """
model_provider = "corp"

[model_providers.corp]
base_url = "https://images.example.test/v1"
experimental_bearer_token = "configured-token"
""",
            )
            with mock.patch.dict(
                os.environ,
                {"CODEX_HOME": str(codex_home)},
                clear=True,
            ):
                resolved = image_gen._resolve_image_api_client_config()

        self.assertEqual(resolved.api_key, "configured-token")
        self.assertIn("experimental_bearer_token", resolved.api_key_source)

    def test_custom_provider_env_key_precedes_configured_bearer_token(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            self.write_config(
                codex_home,
                """
model_provider = "corp"

[model_providers.corp]
env_key = "CORP_IMAGE_API_KEY"
experimental_bearer_token = "fallback-token"
requires_openai_auth = true
""",
            )
            with mock.patch.dict(
                os.environ,
                {
                    "CODEX_HOME": str(codex_home),
                    "CORP_IMAGE_API_KEY": "env-token",
                },
                clear=True,
            ):
                resolved = image_gen._resolve_image_api_client_config()

        self.assertEqual(resolved.api_key, "env-token")
        self.assertIn("CORP_IMAGE_API_KEY", resolved.api_key_source)

    def test_custom_provider_can_use_codex_api_key_auth(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            self.write_config(
                codex_home,
                """
model_provider = "corp"
cli_auth_credentials_store = "file"

[model_providers.corp]
base_url = "https://images.example.test/v1"
requires_openai_auth = true
""",
            )
            self.write_auth(
                codex_home,
                {"auth_mode": "apikey", "OPENAI_API_KEY": "stored-key"},
            )
            with mock.patch.dict(
                os.environ,
                {"CODEX_HOME": str(codex_home)},
                clear=True,
            ):
                resolved = image_gen._resolve_image_api_client_config()

        self.assertEqual(resolved.api_key, "stored-key")
        self.assertIn("auth.json", resolved.api_key_source)

    def test_custom_provider_supports_auth_command(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            (codex_home / "print_token.py").write_text(
                "print('command-token')\n",
                encoding="utf-8",
            )
            self.write_config(
                codex_home,
                f"""
model_provider = "corp"

[model_providers.corp]
base_url = "https://images.example.test/v1"

[model_providers.corp.auth]
command = {json.dumps(sys.executable)}
args = ["print_token.py"]
cwd = "."
timeout_ms = 5000
""",
            )
            with mock.patch.dict(
                os.environ,
                {"CODEX_HOME": str(codex_home)},
                clear=True,
            ):
                resolved = image_gen._resolve_image_api_client_config()

        self.assertEqual(resolved.api_key, "command-token")
        self.assertIn("auth.command", resolved.api_key_source)

    def test_custom_provider_can_use_header_only_auth(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            self.write_config(
                codex_home,
                """
model_provider = "azure-images"

[model_providers.azure-images]
base_url = "https://azure.example.test/openai"
query_params = { api-version = "2025-04-01-preview" }
env_http_headers = { "api-key" = "AZURE_OPENAI_API_KEY" }
""",
            )
            with mock.patch.dict(
                os.environ,
                {
                    "CODEX_HOME": str(codex_home),
                    "AZURE_OPENAI_API_KEY": "azure-key",
                },
                clear=True,
            ):
                resolved = image_gen._resolve_image_api_client_config()

        self.assertIsNone(resolved.api_key)
        self.assertEqual(resolved.default_headers, {"api-key": "azure-key"})
        self.assertEqual(
            resolved.default_query,
            {"api-version": "2025-04-01-preview"},
        )

    def test_amazon_bedrock_provider_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir)
            self.write_config(codex_home, 'model_provider = "amazon-bedrock"\n')
            with mock.patch.dict(
                os.environ,
                {"CODEX_HOME": str(codex_home)},
                clear=True,
            ):
                with self.assertRaises(image_gen.CredentialResolutionError) as raised:
                    image_gen._resolve_image_api_client_config()

        self.assertIn("AWS authentication", str(raised.exception))

    def test_async_client_receives_resolved_configuration(self) -> None:
        captured = {}

        class FakeAsyncOpenAI:
            def __init__(self, **kwargs):
                captured.update(kwargs)

        fake_openai = types.ModuleType("openai")
        fake_openai.AsyncOpenAI = FakeAsyncOpenAI
        resolved = image_gen.ImageAPIClientConfig(
            provider_id="corp",
            api_key_source="test",
            api_key="sk-test",
            base_url="https://example.test/v1",
            default_headers={"X-Test": "yes"},
            default_query={"region": "test"},
            max_retries=9,
        )

        with mock.patch.dict(sys.modules, {"openai": fake_openai}):
            with mock.patch.object(
                image_gen,
                "_resolve_image_api_client_config",
                return_value=resolved,
            ):
                client = image_gen._create_async_client()

        self.assertIsInstance(client, FakeAsyncOpenAI)
        self.assertEqual(
            captured,
            {
                "api_key": "sk-test",
                "base_url": "https://example.test/v1",
                "default_headers": {"X-Test": "yes"},
                "default_query": {"region": "test"},
                "max_retries": 9,
            },
        )

    def test_header_only_client_disables_sdk_bearer_auth(self) -> None:
        captured = {}

        class FakeAsyncOpenAI:
            def __init__(self, **kwargs):
                captured.update(kwargs)

        fake_openai = types.ModuleType("openai")
        fake_openai.AsyncOpenAI = FakeAsyncOpenAI
        resolved = image_gen.ImageAPIClientConfig(
            provider_id="azure-images",
            api_key_source="configured provider headers",
            default_headers={"api-key": "azure-key"},
        )

        with mock.patch.dict(sys.modules, {"openai": fake_openai}):
            with mock.patch.object(
                image_gen,
                "_resolve_image_api_client_config",
                return_value=resolved,
            ):
                image_gen._create_async_client()

        self.assertEqual(captured["api_key"], "")
        self.assertFalse(captured["_enforce_credentials"])
        self.assertEqual(captured["default_headers"], {"api-key": "azure-key"})

    def test_all_live_api_commands_are_async(self) -> None:
        self.assertTrue(inspect.iscoroutinefunction(image_gen._generate))
        self.assertTrue(inspect.iscoroutinefunction(image_gen._edit))
        self.assertTrue(inspect.iscoroutinefunction(image_gen._run_generate_batch))


if __name__ == "__main__":
    unittest.main()
