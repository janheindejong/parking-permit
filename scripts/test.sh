set -ex

export PREFIX=".venv/bin/"
export SOURCE_FILES="parking_permit tests"

${PREFIX}black --check --diff $SOURCE_FILES
${PREFIX}mypy $SOURCE_FILES
${PREFIX}pytest