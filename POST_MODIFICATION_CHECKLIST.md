# Post-Modification Checklist

Run the following commands after every code modification:

```bash
poetry run pytest
poetry run pytest -m unit
poetry run pytest -m integration
poetry run pytest -m e2e
poetry run ruff check .
poetry run ruff format .
poetry run mypy app
```

Expected workflow:

1. Run the full command set above after making changes.
2. If any command reports errors or failures, fix them.
3. Re-run the relevant commands until the checks pass.
4. Do not treat the modification as complete until the required checks are clean, unless an intentional exception is documented.
