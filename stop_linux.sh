echo "Stopping Kouchou-AI..."

if ! docker info > /dev/null 2>&1; then
  echo "Docker is not running."
  echo "Please start Docker and try again."
  read -p "Press Enter to exit..."
  exit 1
fi

docker compose down

echo ""
echo "Kouchou-AI has been stopped."
echo ""
