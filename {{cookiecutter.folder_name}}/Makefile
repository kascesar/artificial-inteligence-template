DOCS_OUTPUT_DIR = docs/
DOCS_LOGO_URL = https://www.python.org/static/img/python-logo.png

.PHONY: help docs

# Target por defecto que muestra la ayuda
help:
	@echo "Uso: make [target]"
	@echo ""
	@echo "Targets disponibles:"
	@echo "  docs     Genera la documentación con pdoc"
	@echo "  help     Muestra este mensaje de ayuda"

docs:
	pdoc --mermaid --math src -o $(DOCS_OUTPUT_DIR) --logo $(DOCS_LOGO_URL)
