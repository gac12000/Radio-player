from flask import Flask, render_template_string, Response, request
import requests

app = Flask(__name__)

# Diseño minimalista "Canon" integrado
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>RADIOS.KESUG.COM</title>
    <style>
        :root { --accent: #c41230; }
        body { font-family: "Segoe UI", sans-serif; background: #fff; margin: 0; }
        header { position: sticky; top: 0; background: #000; padding: 20px; z-index: 100; text-align: center; border-bottom: 4px solid var(--accent); }
        header h1 { color: #fff; font-size: 18px; margin: 0; letter-spacing: 2px; font-weight: 900; text-transform: uppercase; }
        header h1 span { color: var(--accent); }
        .container { max-width: 600px; margin: 0 auto; padding-bottom: 50px; }
        .card { padding: 30px 20px; border-bottom: 1px solid #eee; }
        .meta { font-size: 11px; font-weight: 700; color: var(--accent); text-transform: uppercase; margin-bottom: 5px; display: block; }
        .name { font-size: 26px; font-weight: 800; margin: 0 0 15px 0; letter-spacing: -1px; line-height: 1.1; }
        audio { width: 100%; height: 35px; }
        .mix-container { height: 580px; margin-top: 20px; border: 1px solid #eee; }
        iframe { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>
    <header><h1>RADIOS<span>.KESUG.COM</span></h1></header>
    <div class="container">
        {% for radio in radios %}
        <div class="card">
            <span class="meta">{{ radio.genero }} / {{ radio.idioma }}</span>
            <h2 class="name">{{ radio.nombre }}</h2>
            {% if 'mixcloud.com' in radio.url %}
                <div class="mix-container">
                    <iframe src="https://www.mixcloud.com/widget/iframe/?hide_cover=1&light=1&limit=10&feed={{ radio.url|urlencode }}"></iframe>
                </div>
            {% else %}
                <audio controls preload="none">
                    <source src="/proxy?url={{ radio.url|urlencode }}" type="audio/mpeg">
                </audio>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    radios = []
    try:
        with open('radios.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    radios.append({
                        'nombre': parts[0],
                        'genero': parts[1],
                        'idioma': parts[2],
                        'url': parts[3]
                    })
    except:
        pass
    return render_template_string(HTML_TEMPLATE, radios=radios)

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    def generate():
        r = requests.get(url, stream=True, timeout=10)
        for chunk in r.iter_content(chunk_size=16384):
            yield chunk
    return Response(generate(), mimetype="audio/mpeg")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
