curl -X POST "base_url/send-email/" \
-H "Content-Type: application/json" \
-H "smtp-username: your-email@gmail.com" \
-H "smtp-password: your-app-password" \
-d '{
  "subject": "Test Email",
  "body": "This is a test email sent via the Mail Delivery Service API.",
  "recipient_email": "recipient@example.com"
}'
