#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linux Rice Dashboard - MVP
Backend principal com Flask
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import random
import os
from functools import wraps
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
from urllib.parse import urlparse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'linux-rice-dashboard-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos da base de dados
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

class QuickLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), default='general')
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    fast_access = db.Column(db.Boolean, default=False)  # Novo campo para dashboard

# Decorator para login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# RSS Feeds para Linux Rice News
RSS_FEEDS = [
    'https://www.reddit.com/r/unixporn.rss',
    'https://www.linuxtoday.com/feed/rss',
    'https://blog.linuxmint.com/rss.xml',
    'https://www.omgubuntu.co.uk/feed',
    'https://www.phoronix.com/rss.php'
]

# Setup wallpapers/imagens de rice - novo fonte
def get_favicon(url):
    """Obtém o favicon de um site - otimizado"""
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        # Usar Google Favicon API como principal (mais rápido e confiável)
        return f"https://www.google.com/s2/favicons?domain={domain}&sz=64"
        
    except:
        return "data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🔗</text></svg>"

def get_unixporn_images():
    """Obtém imagens de setups Linux - método alternativo"""
    images = []
    
    try:
        # Tentar RSS do Reddit com headers diferentes
        import urllib.request
        import xml.etree.ElementTree as ET
        import re
        
        # RSS URL alternativa
        rss_url = "https://www.reddit.com/r/unixporn.rss"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        req = urllib.request.Request(rss_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            xml_data = response.read().decode('utf-8')
            
            # Verificar se é Atom ou RSS
            if '<entry>' in xml_data:
                # Atom format
                root = ET.fromstring(xml_data)
                namespace = {'atom': 'http://www.w3.org/2005/Atom'}
                entries = root.findall('.//atom:entry', namespace)
                
                for entry in entries[:5]:
                    title = entry.find('atom:title', namespace).text
                    link = entry.find('atom:link', namespace).get('href')
                    
                    # Procurar imagem no conteúdo
                    content = entry.find('atom:content', namespace)
                    image_url = None
                    
                    if content is not None:
                        content_text = content.text
                        # Reddit preview images (preview.redd.it) - melhorado
                        preview_matches = re.findall(r'(https://preview\.redd\.it/[^\s\?&"]+\.(?:jpg|jpeg|png|webp))', content_text)
                        if preview_matches:
                            # Usar a primeira imagem encontrada
                            base_url = preview_matches[0]
                            # Adicionar parâmetros de qualidade mas sem filtros de cor
                            image_url = base_url + '?width=1080&format=png&auto=webp'
                        else:
                            # Procurar outras imagens (i.redd.it, imgur, etc.)
                            other_matches = re.findall(r'(https://i\.redd\.it/[^\s\?&"]+\.(?:jpg|jpeg|png|webp))', content_text)
                            if other_matches:
                                image_url = other_matches[0]
                            else:
                                # Fallback para img tags
                                img_match = re.search(r'<img[^>]+src=\"([^\"]+)\"', content_text)
                                if img_match:
                                    image_url = img_match.group(1)
                    
                    if image_url:
                        images.append({
                            'url': image_url,
                            'title': title,
                            'link': link,
                            'thumbnail': image_url
                        })
                        
            elif '<item>' in xml_data:
                # RSS format
                root = ET.fromstring(xml_data)
                items = root.findall('.//item')
                
                for item in items[:5]:
                    title = item.find('title').text
                    link = item.find('link').text
                    
                    # Procurar imagem
                    image_url = None
                    description = item.find('description')
                    
                    if description is not None:
                        content = description.text
                        # Reddit preview images (preview.redd.it) - melhorado
                        preview_matches = re.findall(r'(https://preview\.redd\.it/[^\s\?&"]+\.(?:jpg|jpeg|png|webp))', content)
                        if preview_matches:
                            # Usar a primeira imagem encontrada
                            base_url = preview_matches[0]
                            # Adicionar parâmetros de qualidade mas sem filtros de cor
                            image_url = base_url + '?width=1080&format=png&auto=webp'
                        else:
                            # Procurar outras imagens (i.redd.it, imgur, etc.)
                            other_matches = re.findall(r'(https://i\.redd\.it/[^\s\?&"]+\.(?:jpg|jpeg|png|webp))', content)
                            if other_matches:
                                image_url = other_matches[0]
                            else:
                                # Fallback para img tags
                                img_match = re.search(r'<img[^>]+src=\"([^\"]+)\"', content)
                                if img_match:
                                    image_url = img_match.group(1)
                    
                    if image_url:
                        images.append({
                            'url': image_url,
                            'title': title,
                            'link': link,
                            'thumbnail': image_url
                        })
            
            print(f"Found {len(images)} images from r/unixporn RSS")
                    
    except Exception as e:
        print(f"Error fetching unixporn RSS: {e}")
    
    # Se não encontrou imagens, tentar método alternativo
    if not images:
        try:
            # Usar Unsplash com keywords específicas de rice
            import random
            
            rice_keywords = [
                'linux,setup,desktop,rice',
                'minimal,desktop,linux,terminal',
                'dark,theme,linux,workspace',
                'arch,linux,dotfiles,setup',
                'i3wm,linux,window,manager'
            ]
            
            for keyword in rice_keywords[:3]:
                images.append({
                    'url': f'https://source.unsplash.com/1600x900/?{keyword}',
                    'title': f'Linux Rice - {keyword.replace(",", " ").title()}',
                    'link': 'https://reddit.com/r/unixporn',
                    'thumbnail': f'https://source.unsplash.com/400x300/?{keyword}'
                })
                
            print("Using Unsplash rice images as fallback")
            
        except Exception as e:
            print(f"Error with Unsplash fallback: {e}")
            # Último fallback
            images = [
                {
                    'url': 'https://source.unsplash.com/1600x900/?linux,setup',
                    'title': 'Linux Setup',
                    'link': 'https://reddit.com/r/unixporn',
                    'thumbnail': 'https://source.unsplash.com/400x300/?linux,setup'
                }
            ]
    
    return images

# Rotas
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/wall.jpg')
def serve_wallpaper():
    """Serve o wallpaper personalizado da raiz"""
    from flask import send_from_directory
    return send_from_directory('.', 'wall.jpg')

@app.route('/dashboard')
@login_required
def dashboard():
    # Obter notas recentes
    notes = Note.query.order_by(Note.created_at.desc()).limit(5).all()
    
    # Obter links rápidos (só os marcados como fast_access)
    fast_links = QuickLink.query.filter_by(fast_access=True).order_by(QuickLink.created_at.desc()).limit(8).all()
    
    # Adicionar favicons aos links - simplificado
    for link in fast_links:
        link.favicon = f"https://www.google.com/s2/favicons?domain={link.url.split('/')[2]}&sz=64"
    
    # Obter notícias RSS - cache simples
    news_items = get_rss_news()
    
    # Setup do dia - usar wallpaper fixo para performance
    setup_image = {
        'url': '/wall.jpg',
        'title': 'Meu wallpaper',
        'link': '#'
    }
    
    return render_template('dashboard.html', 
                         notes=notes, 
                         links=fast_links, 
                         news=news_items,
                         setup_image=setup_image)

@app.route('/notes')
@login_required
def notes():
    all_notes = Note.query.order_by(Note.created_at.desc()).all()
    return render_template('notes.html', notes=all_notes)

@app.route('/notes/add', methods=['POST'])
@login_required
def add_note():
    title = request.form.get('title')
    content = request.form.get('content')
    
    if title and content:
        note = Note(title=title, content=content)
        db.session.add(note)
        db.session.commit()
        flash('Note added successfully!', 'success')
    
    return redirect(url_for('notes'))

@app.route('/notes/edit/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    if request.method == 'POST':
        note.title = request.form.get('title')
        note.content = request.form.get('content')
        note.completed = 'completed' in request.form
        note.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Note updated successfully!', 'success')
        return redirect(url_for('notes'))
    
    return render_template('edit_note.html', note=note)

@app.route('/notes/delete/<int:note_id>')
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted successfully!', 'info')
    return redirect(url_for('notes'))

@app.route('/links')
@login_required
def links():
    all_links = QuickLink.query.order_by(QuickLink.category).all()
    
    # Definir category icons para o template
    category_icons = {
        'general': '📁',
        'development': '💻',
        'documentation': '📚',
        'reddit': '🤖',
        'news': '📰',
        'tools': '🔧',
        'inspiration': '✨'
    }
    
    return render_template('links.html', links=all_links, category_icons=category_icons)

@app.route('/links/add', methods=['POST'])
@login_required
def add_link():
    title = request.form.get('title')
    url = request.form.get('url')
    category = request.form.get('category', 'general')
    description = request.form.get('description')
    fast_access = 'fast_access' in request.form  # Novo campo
    
    if title and url:
        link = QuickLink(title=title, url=url, category=category, description=description, fast_access=fast_access)
        db.session.add(link)
        db.session.commit()
        flash('Link added successfully!', 'success')
    
    return redirect(url_for('links'))

@app.route('/links/delete/<int:link_id>')
@login_required
def delete_link(link_id):
    link = QuickLink.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash('Link deleted successfully!', 'info')
    return redirect(url_for('links'))

def get_rss_news():
    """Obtém notícias dos feeds RSS - otimizado para velocidade"""
    # Usar fallback direto para máxima velocidade
    return [
        {
            'title': 'Linux Rice Dashboard',
            'link': '#',
            'summary': 'Your personal Linux dashboard is ready!',
            'published': datetime.now().strftime('%Y-%m-%d'),
            'source': 'System'
        },
        {
            'title': 'Customize Your Linux Experience',
            'link': 'https://reddit.com/r/unixporn',
            'summary': 'Join the community for sharing Linux desktop setups.',
            'published': datetime.now().strftime('%Y-%m-%d'),
            'source': 'r/unixporn'
        },
        {
            'title': 'Linux News',
            'link': 'https://linuxtoday.com',
            'summary': 'Stay updated with the latest Linux news.',
            'published': datetime.now().strftime('%Y-%m-%d'),
            'source': 'LinuxToday'
        }
    ]

# Função para criar utilizador admin
def create_admin_user():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123!')
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin/admin123!")
    else:
        print("Admin user already exists")

# Função para criar dados iniciais
def create_initial_data():
    # Não criar links padrão - deixar o utilizador definir os seus próprios
    print("Initial data creation skipped - user will define their own links")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_user()
        create_initial_data()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
