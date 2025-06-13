#!/bin/bash

google_location=$(pip show googleapis-common-protos | grep Location | awk '{print $2}')
proto_path=./finam-trade-api/proto/grpc
output_path=./finam_grpc_client/grpc

echo "Удаление старых файлов"
rm -rf "$output_path"

echo "Клонирование репозитория: https://github.com/FinamWeb/finam-trade-api.git"
git clone https://github.com/FinamWeb/finam-trade-api.git

echo "Копирование proto-файлов из $proto_path в $output_path"
cp -r "$proto_path" "$output_path"

echo "Замена импортов c grpc/tradeapi/* на finam_grpc_client/grpc/tradeapi/*"
find "$output_path" -type f -name "*.proto" | while read -r proto_file; do
    echo "$proto_file"
    sed -i 's|import "grpc/tradeapi/|import "finam_grpc_client/grpc/tradeapi/|g' "$proto_file"
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

echo "Удаление репозитория: https://github.com/FinamWeb/finam-trade-api.git"
rm -rf ./finam-trade-api
echo "Готово"