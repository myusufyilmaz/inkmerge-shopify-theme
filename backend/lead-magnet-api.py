#!/usr/bin/env python3
"""
InkMerge Lead Magnet API
Handles form submissions and integrates with Acumbamail
"""

import os
import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

ACUMBAMAIL_API_TOKEN = os.getenv('ACUMBAMAIL_API_TOKEN')
ACUMBAMAIL_LIST_ID = os.getenv('ACUMBAMAIL_LIST_ID', '1')  # Default to list 1
PORT = 5000

class LeadMagnetHandler(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        """Handle preflight CORS requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path.startswith('/thank-you'):
            self.serve_thank_you_page()
        elif self.path in ['/', '/landing']:
            self.serve_landing_page()
        elif self.path in ['/guide', '/dtf-application-guide']:
            self.serve_application_guide()
        elif self.path in ['/indexnow', '/indexnow-submit']:
            self.serve_indexnow_interface()
        elif self.path.startswith('/api/indexnow/submit'):
            self.handle_indexnow_get_submission()
        elif self.path == '/download-project':
            self.serve_project_download()
        else:
            self.send_error_response(404, 'Not found')
    
    def serve_landing_page(self):
        """Serve the landing page"""
        try:
            with open('backend/landing-page.html', 'r') as f:
                html_content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        except Exception as e:
            print(f'Error serving landing page: {e}')
            self.send_error_response(500, 'Error loading page')
    
    def serve_application_guide(self):
        """Serve the comprehensive DTF application guide"""
        try:
            with open('backend/dtf-application-guide.html', 'r') as f:
                html_content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'public, max-age=3600')  # Cache for 1 hour
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        except Exception as e:
            print(f'Error serving application guide: {e}')
            self.send_error_response(500, 'Error loading guide')
    
    def serve_indexnow_interface(self):
        """Serve the IndexNow URL submission interface"""
        try:
            with open('backend/indexnow-submit-interface.html', 'r') as f:
                html_content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        except Exception as e:
            print(f'Error serving IndexNow interface: {e}')
            self.send_error_response(500, 'Error loading page')
    
    def serve_thank_you_page(self):
        """Serve the thank-you page"""
        try:
            # Parse query parameters
            from urllib.parse import parse_qs, urlparse
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)
            email = params.get('email', [''])[0]
            name = params.get('name', [''])[0]
            
            # Read and serve the thank-you HTML template
            with open('backend/thank-you.html', 'r') as f:
                html_content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        except Exception as e:
            print(f'Error serving thank-you page: {e}')
            self.send_error_response(500, 'Error loading page')
    
    def serve_project_download(self):
        """Serve the project archive download"""
        try:
            archive_path = 'inkmerge-project.tar.gz'
            
            with open(archive_path, 'rb') as f:
                file_content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/gzip')
            self.send_header('Content-Disposition', 'attachment; filename="inkmerge-project.tar.gz"')
            self.send_header('Content-Length', str(len(file_content)))
            self.end_headers()
            self.wfile.write(file_content)
            
            print(f'✅ Project download served successfully ({len(file_content)} bytes)')
        except Exception as e:
            print(f'Error serving project download: {e}')
            self.send_error_response(500, 'Error downloading project')
    
    def do_POST(self):
        """Handle form submissions and API requests"""
        if self.path == '/api/indexnow/submit':
            self.handle_indexnow_submission()
        elif self.path == '/apps/inkmerge-leads/submit':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                # Extract form data
                first_name = data.get('first_name', '').strip()
                email = data.get('email', '').strip()
                business_type = data.get('business_type', '')
                consent = data.get('consent', False)
                
                # Validate required fields
                if not first_name or not email or not consent:
                    self.send_error_response(400, 'Missing required fields')
                    return
                
                # Add to Acumbamail
                success = self.add_to_acumbamail(first_name, email, business_type)
                
                if success:
                    self.send_json_response(200, {
                        'success': True,
                        'message': 'Successfully added to email list'
                    })
                else:
                    self.send_error_response(500, 'Failed to add to email list')
                    
            except Exception as e:
                print(f'Error processing submission: {e}')
                self.send_error_response(500, str(e))
        else:
            self.send_error_response(404, 'Not found')
    
    def add_to_acumbamail(self, first_name, email, business_type):
        """Add subscriber to Acumbamail list"""
        try:
            # Acumbamail API endpoint
            url = 'https://acumbamail.com/api/1/addSubscriber/'
            
            print(f'🔍 DEBUG: Adding subscriber...')
            print(f'  First Name: {first_name}')
            print(f'  Email: {email}')
            print(f'  Business Type: {business_type}')
            print(f'  List ID: {ACUMBAMAIL_LIST_ID}')
            
            # Prepare subscriber data (Acumbamail expects form data with email inside merge_fields)
            payload = {
                'auth_token': ACUMBAMAIL_API_TOKEN,
                'list_id': ACUMBAMAIL_LIST_ID,
                'merge_fields[email]': email,
                'merge_fields[FNAME]': first_name,
                'merge_fields[BUSINESS_TYPE]': business_type,
                'merge_fields[LEAD_MAGNET]': 'DTF Application Guide',
                'merge_fields[SOURCE]': 'Landing Page',
                'double_optin': '0',
                'welcome_email': '1'
            }
            
            print(f'📤 Sending to Acumbamail: {url}')
            response = requests.post(url, data=payload, timeout=10)
            print(f'📥 Response status: {response.status_code}')
            print(f'📥 Response body: {response.text}')
            
            if response.status_code in [200, 201]:
                result = response.json()
                print(f'✅ Added {email} to Acumbamail list (ID: {result.get("subscriber_id")})')
                return True
            elif response.status_code == 400:
                # Check if it's a duplicate subscriber (already exists)
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', '').lower()
                    if 'already exists' in error_msg:
                        print(f'ℹ️  {email} already subscribed (treating as success)')
                        return True
                except:
                    pass
                print(f'❌ Acumbamail error: {response.status_code} - {response.text}')
                return False
            else:
                print(f'❌ Acumbamail error: {response.status_code} - {response.text}')
                return False
                
        except Exception as e:
            print(f'❌ Error adding to Acumbamail: {e}')
            return False
    
    def normalize_url(self, url):
        """Normalize URL to use www.inkmerge.com"""
        if not url.startswith('http'):
            url = 'https://' + url
        # Replace inkmerge.com with www.inkmerge.com
        url = url.replace('https://inkmerge.com/', 'https://www.inkmerge.com/')
        url = url.replace('http://inkmerge.com/', 'https://www.inkmerge.com/')
        return url
    
    def validate_url(self, url):
        """Validate URL belongs to inkmerge.com domain"""
        normalized = self.normalize_url(url)
        return normalized.startswith('https://www.inkmerge.com/')
    
    def handle_indexnow_get_submission(self):
        """Handle single URL IndexNow submission via GET"""
        try:
            # Parse query parameters
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)
            url = params.get('url', [''])[0]
            
            if not url:
                self.send_error_response(400, 'No URL provided')
                return
            
            # Validate and normalize URL
            if not self.validate_url(url):
                self.send_error_response(400, 'URL must be from inkmerge.com domain')
                return
            
            normalized_url = self.normalize_url(url)
            
            # Import and submit
            import sys
            import os
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from indexnow_submit import submit_single_url
            
            result = submit_single_url(normalized_url)
            
            if result['success']:
                self.send_json_response(200, result)
            else:
                self.send_json_response(result['status_code'] or 422, result)
                
        except Exception as e:
            print(f'❌ Error handling IndexNow GET submission: {e}')
            self.send_error_response(500, str(e))
    
    def handle_indexnow_submission(self):
        """Handle IndexNow URL submission via POST (bulk)"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            urls = data.get('urls', [])
            
            if not urls:
                self.send_error_response(400, 'No URLs provided')
                return
            
            # Validate and normalize all URLs
            validated_urls = []
            for url in urls:
                if not self.validate_url(url):
                    self.send_error_response(400, f'Invalid URL: {url} (must be from inkmerge.com)')
                    return
                validated_urls.append(self.normalize_url(url))
            
            # Import the IndexNow submission function
            import sys
            import os
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from indexnow_submit import submit_bulk_urls
            
            result = submit_bulk_urls(validated_urls)
            
            if result['success']:
                self.send_json_response(200, result)
            else:
                self.send_json_response(422, result)
                
        except Exception as e:
            print(f'❌ Error handling IndexNow submission: {e}')
            self.send_error_response(500, str(e))
    
    def send_json_response(self, status_code, data):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def send_error_response(self, status_code, message):
        """Send error response"""
        self.send_json_response(status_code, {
            'success': False,
            'error': message
        })
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f'[{self.address_string()}] {format % args}')


def main():
    print('=' * 70)
    print('InkMerge Lead Magnet API Server')
    print('=' * 70)
    print()
    print(f'🚀 Starting server on port {PORT}...')
    print(f'📧 Acumbamail List ID: {ACUMBAMAIL_LIST_ID}')
    token_status = '✅ Configured' if ACUMBAMAIL_API_TOKEN else '❌ Missing'
    print(f'🔑 API Token: {token_status}')
    print()
    print(f'📍 Endpoint: http://localhost:{PORT}/apps/inkmerge-leads/submit')
    print()
    print('Waiting for form submissions...')
    print()
    
    server = HTTPServer(('0.0.0.0', PORT), LeadMagnetHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n\n⛔ Shutting down server...')
        server.shutdown()


if __name__ == '__main__':
    main()
