echo "Starting Kouchou-AI..."

if ! docker info > /dev/null 2>&1; then
  echo "Docker is not running."
  echo "Please start Docker and try again."
  read -p "Press Enter to exit..."
  exit 1
fi

docker compose up -d

echo ""
echo "Kouchou-AI is now running!"
echo "You can access the following URLs in your browser:"
echo "  http://localhost:3000 - Report Viewer"
echo "  http://localhost:4000 - Admin Panel"
echo ""
