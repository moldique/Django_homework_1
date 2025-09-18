import http.server
import socketserver
import os
from urllib.parse import urlparse

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Парсим URL
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Если запрашивается CSS файл, отдаем его
        if path.endswith('.css'):
            self.serve_css_file(path)
            return
            
        # На любой другой GET-запрос возвращаем страницу контактов
        self.serve_contacts_page()
    
    def do_POST(self):
        """Обрабатывает POST-запросы"""
        # Получаем длину контента
        content_length = int(self.headers.get('Content-Length', 0))
        
        if content_length > 0:
            # Читаем данные из тела запроса
            post_data = self.rfile.read(content_length)
            
            # Декодируем данные
            try:
                decoded_data = post_data.decode('utf-8')
                print("=" * 50)
                print("POST-запрос получен!")
                print(f"Заголовки:")
                for header, value in self.headers.items():
                    print(f"  {header}: {value}")
                print(f"Данные от пользователя:")
                print(f"  {decoded_data}")
                print("=" * 50)
            except UnicodeDecodeError:
                print("=" * 50)
                print("POST-запрос получен!")
                print(f"Данные (бинарные): {post_data}")
                print("=" * 50)
        else:
            print("=" * 50)
            print("POST-запрос получен (пустое тело)!")
            print("=" * 50)
        
        # Отправляем ответ (страницу контактов)
        self.serve_contacts_page()
    
    def serve_css_file(self, path):
        """Отдает CSS файлы"""
        css_path = path.lstrip('/')
        if os.path.exists(css_path):
            with open(css_path, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.send_header('Content-length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "CSS file not found")
    
    def serve_contacts_page(self):
        """Отдает страницу контактов"""
        try:
            # Читаем HTML файл контактов
            with open('contacts.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Отправляем ответ
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-length', str(len(html_content.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
        except FileNotFoundError:
            self.send_error(404, "contacts.html not found")
        except Exception as e:
            self.send_error(500, f"Error reading file: {str(e)}")

def run_server(port=8000):
    """Запускает веб-сервер"""
    with socketserver.TCPServer(("", port), MyHandler) as httpd:
        print(f"Сервер запущен на порту {port}")
        print(f"Откройте http://localhost:{port} в браузере")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nСервер остановлен")

if __name__ == "__main__":
    run_server()
