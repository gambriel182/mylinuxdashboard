# 🐧 Linux Rice Dashboard - MVP

Um painel de administração pessoal com estética terminal/tech para organizar informações e conteúdos de interesse Linux.

## 🚀 Funcionalidades

### 🔐 Autenticação
- Sistema de login seguro com Flask
- Sessão protegida com SQLite
- Utilizador admin padrão: `admin` / `admin123`

### 📊 Dashboard Principal
- **Setup do Dia**: Wallpaper inspirador de setups Linux
- **Notas Rápidas**: Sistema de to-do list com gestão completa
- **Linux Rice News**: RSS feeds de sites de customização Linux
- **Links Rápidos**: Favoritos organizados por categorias
- **Status do Sistema**: Informações em tempo real
- **Terminal Output**: Simulação de terminal com animações

### 📝 Módulo de Notas
- Criar, editar, apagar notas
- Marcar tarefas como concluídas
- Auto-save e recuperação de drafts
- Estatísticas de produtividade

### 🔗 Módulo de Links
- Organizar favoritos por categorias
- Copiar URLs com um clique
- Detecção automática de categorias
- Busca integrada (para >10 links)

### 📰 Módulo de Notícias
- RSS feeds de:
  - r/unixporn
  - Arch Linux News
  - Linux Mint Blog
  - OMG! Ubuntu
  - Phoronix
- Atualização automática a cada 5 minutos

## 🛠️ Tecnologias

- **Backend**: Python 3.8+ com Flask
- **Database**: SQLite (leve e portátil)
- **Frontend**: HTML5 + CSS3 + Jinja2
- **Feeds**: feedparser para RSS
- **Estilo**: Terminal-inspired dark theme

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gestor de pacotes Python)

### Passos

1. **Clonar/Download do projeto**
   ```bash
   cd "/home/gambriel182/Documentos/My Linux Dashboard"
   ```

2. **Criar ambiente virtual (recomendado)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Iniciar a aplicação**
   ```bash
   python app.py
   ```

5. **Aceder ao dashboard**
   - Abra o browser em: `http://localhost:5000`
   - Login com: `admin` / `admin123`

## 🎨 Personalização

### Alterar Credenciais
Edite o ficheiro `app.py` na função `create_admin_user()`:
```python
admin = User(
    username='teu_username',
    password_hash=generate_password_hash('tua_password')
)
```

### Adicionar RSS Feeds
Modifique a lista `RSS_FEEDS` em `app.py`:
```python
RSS_FEEDS = [
    'https://www.reddit.com/r/unixporn.rss',
    'https://archlinux.org/feeds/news/',
    # Adiciona mais feeds aqui
]
```

### Customizar Wallpapers
Altere a lista `SETUP_IMAGES` em `app.py`:
```python
SETUP_IMAGES = [
    'https://url-da-imagem-1.jpg',
    'https://url-da-imagem-2.jpg',
    # Adiciona mais imagens
]
```

### Tema e Cores
Edite `static/css/style.css` para personalizar:
- Cores primárias em `:root`
- Fontes e tipografia
- Animações e transições

## 📁 Estrutura do Projeto

```
My Linux Dashboard/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── dashboard.db          # Base de dados SQLite (criado automaticamente)
├── templates/            # Templates Jinja2
│   ├── base.html         # Template base
│   ├── login.html        # Página de login
│   ├── dashboard.html    # Dashboard principal
│   ├── notes.html        # Gestão de notas
│   ├── edit_note.html    # Edição de notas
│   └── links.html        # Gestão de links
├── static/
│   └── css/
│       └── style.css     # Estilos principais
└── README.md            # Este ficheiro
```

## 🚀 Uso e Funcionalidades

### Dashboard
- **Cards responsivos** com layout grid
- **Atualizações em tempo real** de status
- **Animações suaves** e efeitos hover
- **Design responsivo** para mobile

### Notas
- **Atalhos de teclado**:
  - `Ctrl+N`: Nova nota
  - `Ctrl+S`: Salvar (no editor)
  - `Escape`: Cancelar/Voltar
- **Auto-save** automático a cada 2 segundos
- **Recuperação** de drafts não salvos

### Links
- **Atalhos de teclado**:
  - `Ctrl+L`: Novo link
  - `Escape`: Fechar formulário
- **Detecção automática** de categorias por URL
- **Copy-to-clipboard** com feedback visual

## 🔧 Configuração Avançada

### Variáveis de Ambiente
Pode configurar através de environment variables:
```bash
export FLASK_ENV=development
export SECRET_KEY='tua-secret-key'
export DATABASE_URL='sqlite:///dashboard.db'
```

### Deploy
Para produção:
1. Use um WSGI server (Gunicorn, uWSGI)
2. Configure reverse proxy (Nginx)
3. Use HTTPS
4. Configure backup da base de dados

## 🐛 Troubleshooting

### Problemas Comuns

**Porta 5000 em uso:**
```bash
# Use outra porta
python app.py  # Edite app.py para mudar a porta
```

**Permissões SQLite:**
```bash
# Garanta permissões de escrita
chmod 755 "/home/gambriel182/Documentos/My Linux Dashboard"
```

**Dependências em falta:**
```bash
# Reinstale tudo
pip install --upgrade -r requirements.txt
```

### Logs e Debug
- Modo debug ativado por defeito
- Logs de erro no terminal
- Database em `dashboard.db`

## 🤝 Contribuir

1. Fork do projeto
2. Create feature branch: `git checkout -b nova-feature`
3. Commit changes: `git commit -am 'Add nova feature'`
4. Push: `git push origin nova-feature`
5. Submit pull request

## 📝 Roadmap Futuro

- [ ] Sistema de tags para notas
- [ ] Export/Import de dados
- [ ] API REST endpoints
- [ ] Dark/Light theme toggle
- [ ] Integração com GitHub API
- [ ] Sistema de notificações
- [ ] Backup automático
- [ ] Multi-user support

## 📄 Licença

MIT License - feel free to use and modify.

## 🙏 Agradecimentos

- Flask framework
- feedparser para RSS
- Comunidade r/unixporn pela inspiração
- Todos os contribuidores de projetos open-source

---

**Made with 🐧❤️ for the Linux rice community**
