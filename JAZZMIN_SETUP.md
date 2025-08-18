# Configuração do Jazzmin no SisEvol

## O que é o Jazzmin?

O Jazzmin é um tema moderno e responsivo para o painel administrativo do Django. Ele oferece uma interface mais elegante e funcional, com recursos como:

- Design moderno e responsivo
- Sidebar navegável
- Ícones FontAwesome
- Temas personalizáveis
- Melhor experiência do usuário

## Instalação Realizada

### 1. Instalação do Pacote
```bash
pip install django-jazzmin
```

### 2. Configuração no settings.py

O Jazzmin foi adicionado ao `INSTALLED_APPS` no início da lista (antes do `django.contrib.admin`):

```python
INSTALLED_APPS = [
    'jazzmin',  # Deve vir antes do django.contrib.admin
    'django.contrib.admin',
    # ... outros apps
]
```

### 3. Configurações Personalizadas

As seguintes configurações foram adicionadas ao `settings.py`:

#### JAZZMIN_SETTINGS
- **site_title**: "SisEvol Admin" - Título da janela
- **site_header**: "SisEvol" - Cabeçalho do site
- **site_brand**: "SisEvol" - Nome da marca
- **site_logo**: "image/LOGO---EVOL.png" - Logo do site
- **welcome_sign**: "Bem-vindo ao Sistema de Evolução" - Mensagem de boas-vindas
- **copyright**: "SisEvol Ltd" - Copyright no rodapé

#### JAZZMIN_UI_TWEAKS
- **theme**: "cosmo" - Tema Bootstrap
- **navbar**: "navbar-dark" - Navbar escura
- **sidebar**: "sidebar-dark-success" - Sidebar escura com destaque verde
- **brand_colour**: "navbar-success" - Cor da marca verde

### 4. Ícones Configurados

Os seguintes ícones foram configurados para os apps:
- **auth**: fas fa-users-cog (Usuários e Grupos)
- **RH**: fas fa-users (Recursos Humanos)
- **links**: fas fa-link (Links)
- **PerfilMenus**: fas fa-bars (Perfil de Menus)
- **Gestao**: fas fa-chart-bar (Gestão)

## Como Acessar

1. Inicie o servidor Django:
   ```bash
   python manage.py runserver
   ```

2. Acesse o painel administrativo:
   ```
   http://localhost:8000/admin/
   ```

## Personalizações Adicionais

### Alterando o Tema

Para alterar o tema, modifique a configuração `theme` em `JAZZMIN_UI_TWEAKS`:

```python
JAZZMIN_UI_TWEAKS = {
    "theme": "cosmo",  # Opções: cosmo, flatly, journal, etc.
}
```

### Adicionando Ícones

Para adicionar ícones para novos apps, adicione na seção `icons`:

```python
"icons": {
    "your_app": "fas fa-icon-name",
}
```

### Customizando Cores

Para alterar as cores, modifique as configurações em `JAZZMIN_UI_TWEAKS`:

```python
JAZZMIN_UI_TWEAKS = {
    "brand_colour": "navbar-success",  # navbar-primary, navbar-info, etc.
    "accent": "accent-teal",  # accent-primary, accent-info, etc.
}
```

## Recursos Disponíveis

- ✅ Interface moderna e responsiva
- ✅ Sidebar navegável com ícones
- ✅ Tema personalizado com cores do SisEvol
- ✅ Logo personalizado
- ✅ Mensagens de boas-vindas em português
- ✅ Suporte a modais para relacionamentos
- ✅ Formulários em abas horizontais
- ✅ Busca integrada

## Solução de Problemas

### Problema: Logo não aparece
- Verifique se o arquivo `LOGO---EVOL.png` existe em `static/image/`
- Execute `python manage.py collectstatic` novamente

### Problema: Estilos não carregam
- Verifique se o `jazzmin` está antes do `django.contrib.admin` no `INSTALLED_APPS`
- Execute `python manage.py collectstatic` para coletar os arquivos estáticos

### Problema: Erro ao iniciar o servidor
- Verifique se o `django-jazzmin` foi instalado corretamente: `pip show django-jazzmin`
- Execute `python manage.py check` para verificar configurações

## Links Úteis

- [Documentação oficial do Jazzmin](https://github.com/farridav/django-jazzmin)
- [Ícones FontAwesome](https://fontawesome.com/icons)
- [Temas Bootstrap](https://bootswatch.com/)

