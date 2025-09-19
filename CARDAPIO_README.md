# Sistema de Cardápio - SisEvol

## Visão Geral

O sistema de cardápio foi desenvolvido como uma aplicação Django moderna e responsiva, integrada ao sistema SisEvol existente. O cardápio oferece uma experiência visual atrativa com design moderno e funcionalidades interativas.

## Funcionalidades

### 🎨 Design Moderno e Responsivo
- Interface limpa e moderna com gradientes e animações
- Design totalmente responsivo para desktop, tablet e mobile
- Cards interativos com efeitos hover
- Cores personalizáveis por categoria

### 📱 Navegação Intuitiva
- Página principal com pratos em destaque
- Categorias organizadas com ícones e cores
- Sistema de breadcrumb para navegação
- Busca em tempo real

### 🍽️ Gestão de Pratos
- Informações detalhadas dos pratos
- Sistema de tags para restrições alimentares
- Níveis de picante visual
- Informações nutricionais (calorias, tempo de preparo)
- Sistema de avaliações

### 🔍 Filtros Avançados
- Filtro por restrições alimentares (vegetariano, vegano, sem glúten, sem lactose)
- Busca por nome, descrição ou ingredientes
- Filtros combináveis

### ⭐ Sistema de Avaliações
- Avaliações com estrelas (1-5)
- Comentários dos clientes
- Média de avaliações por prato
- Sistema de aprovação de avaliações

## Estrutura do Projeto

```
cardapio/
├── models.py              # Modelos de dados
├── views.py               # Views e lógica de negócio
├── urls.py                # Configuração de URLs
├── admin.py               # Interface administrativa
├── apps.py                # Configuração da aplicação
├── management/
│   └── commands/
│       └── popular_cardapio.py  # Comando para popular dados
└── templates/
    └── cardapio/
        ├── index.html          # Página principal
        ├── categoria.html      # Página de categoria
        └── prato.html          # Página de detalhes do prato
```

## Modelos de Dados

### Categoria
- Nome e descrição
- Ícone e cor personalizáveis
- Ordem de exibição
- Status ativo/inativo

### Prato
- Informações básicas (nome, descrição, preço)
- Categoria de pertencimento
- Ingredientes e características
- Restrições alimentares
- Informações nutricionais
- Sistema de destaque
- URL da imagem

### Avaliação
- Nota de 1 a 5 estrelas
- Comentário opcional
- Sistema de aprovação
- Dados do avaliador

## URLs Disponíveis

- `/cardapio/` - Página principal do cardápio
- `/cardapio/categoria/<id>/` - Página de categoria específica
- `/cardapio/prato/<id>/` - Página de detalhes do prato
- `/cardapio/buscar/` - API de busca de pratos

## Como Usar

### 1. Acesso ao Cardápio
- Faça login no sistema SisEvol
- Clique em "Cardápio" no menu lateral
- Navegue pelas categorias ou use a busca

### 2. Administração
- Acesse `/admin/` para gerenciar o cardápio
- Crie categorias com cores e ícones personalizados
- Adicione pratos com todas as informações
- Gerencie avaliações dos clientes

### 3. Personalização
- Cores das categorias podem ser personalizadas no admin
- Ícones utilizam Bootstrap Icons
- Imagens podem ser URLs externas ou uploads locais

## Tecnologias Utilizadas

- **Django 5.1** - Framework web
- **Bootstrap 5** - Framework CSS
- **Bootstrap Icons** - Ícones
- **CSS3** - Estilos customizados
- **JavaScript** - Interatividade
- **SQLite/PostgreSQL** - Banco de dados

## Características Técnicas

### Responsividade
- Mobile-first design
- Breakpoints para tablet e desktop
- Grid system flexível
- Imagens responsivas

### Performance
- Lazy loading de imagens
- Queries otimizadas
- Cache de templates
- Compressão de assets

### Acessibilidade
- Navegação por teclado
- Contraste adequado
- Textos alternativos
- Estrutura semântica

## Dados de Exemplo

O sistema inclui um comando de management para popular dados de exemplo:

```bash
python manage.py popular_cardapio
```

Este comando cria:
- 5 categorias (Entradas, Pratos Principais, Massas, Sobremesas, Bebidas)
- 15 pratos com informações completas
- Imagens de exemplo do Unsplash

## Personalização

### Cores das Categorias
As cores são definidas em hexadecimal no campo `cor` da categoria e aplicadas via CSS custom properties.

### Ícones
Utiliza Bootstrap Icons. Para alterar, modifique o campo `icone` da categoria.

### Layout
O layout pode ser personalizado editando os arquivos CSS nos templates ou criando arquivos CSS separados.

## Integração com SisEvol

O cardápio está totalmente integrado ao sistema SisEvol:
- Usa o template base existente
- Segue o padrão de design do sistema
- Integrado ao menu lateral
- Usa o sistema de autenticação existente

## Próximos Passos

- [ ] Sistema de pedidos online
- [ ] Integração com pagamentos
- [ ] Sistema de delivery
- [ ] App mobile
- [ ] Relatórios de vendas
- [ ] Sistema de promoções
- [ ] Integração com redes sociais

## Suporte

Para dúvidas ou suporte, entre em contato com a equipe de desenvolvimento do SisEvol.
