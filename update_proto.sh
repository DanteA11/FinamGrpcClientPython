#!/bin/bash

google_location=$(pip show googleapis-common-protos | grep Location | awk '{print $2}')
proto_path=./finam-trade-api/proto
output_path=./finam_grpc_client/proto

echo "Удаление старых файлов"
rm -rf "$output_path"

echo "Клонирование репозитория: https://github.com/FinamWeb/finam-trade-api.git"
git clone https://github.com/FinamWeb/finam-trade-api.git

rm -rf "$proto_path/google"
mv "$proto_path/protoc-gen-openapiv2" "$proto_path/protoc_gen_openapiv2"

echo "Копирование proto-файлов из $proto_path в $output_path"
cp -r "$proto_path" "$output_path"

echo "Замена импортов c grpc/* на finam_grpc_client/proto/grpc/*"
find "$output_path" -type f -name "*.proto" | while read -r proto_file; do
    echo "$proto_file"
    sed -i 's|import "grpc/|import "finam_grpc_client/proto/grpc/|g' "$proto_file"
    sed -i 's|import "protoc-gen-openapiv2/|import "finam_grpc_client/proto/protoc_gen_openapiv2/|g' "$proto_file"
done
echo "Замена импортов завершена"

echo "Генерация кода GRPC"
find "$output_path" -name "*.proto" -exec python -m grpc_tools.protoc -I. \
  --python_out=. \
  --mypy_out=. \
  --grpc_python_out=. \
  --proto_path=. \
  --proto_path="$google_location" {} \;
echo "Генерация завершена"
echo "Создание __init__.py в каждой директории"
find $output_path -type d -exec touch {}/__init__.py \;
echo "Завершено"

echo "Удаление репозитория: https://github.com/FinamWeb/finam-trade-api.git"
rm -rf ./finam-trade-api
echo "Готово"