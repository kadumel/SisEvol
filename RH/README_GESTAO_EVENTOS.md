# Sistema de Gestão de Eventos - RH

## Visão Geral

O sistema de gestão de eventos foi criado para permitir o controle e acompanhamento de eventos relacionados aos funcionários da empresa. O sistema inclui funcionalidades completas de CRUD (Create, Read, Update, Delete) para eventos e tipos de eventos.

## Funcionalidades

### 1. Gestão de Eventos (`/gestaoEventos/`)

#### Características:
- **Listagem de eventos** com paginação e ordenação
- **Filtros avançados** por tipo, data e descrição
- **Adição de novos eventos** via modal
- **Edição de eventos** existentes
- **Exclusão de eventos** com confirmação
- **Exportação para Excel** dos dados
- **Visualização completa** de observações

#### Campos do Evento:
- **Tipo**: Relacionado ao modelo TipoEvento
- **Data**: Data do evento
- **Descrição**: Descrição breve do evento (máx. 50 caracteres)
- **Observação**: Observações detalhadas (máx. 250 caracteres)
- **Usuário**: Usuário que criou o evento
- **Timestamps**: Data de criação e atualização

### 2. Gestão de Tipos de Evento (`/gestaoTiposEvento/`)

#### Características:
- **Listagem de tipos** de eventos
- **Adição de novos tipos** via modal
- **Edição de tipos** existentes
- **Exclusão de tipos** com validação de dependências
- **Proteção contra exclusão** de tipos em uso

#### Campos do Tipo de Evento:
- **Tipo de Evento**: Nome do tipo (máx. 40 caracteres)
- **Timestamps**: Data de criação e atualização

## URLs Disponíveis

### Eventos:
- `GET /gestaoEventos/` - Página principal de gestão de eventos
- `POST /addEvento/` - Adicionar novo evento
- `POST /updateEvento/<id>/` - Atualizar evento existente
- `GET /getEvento/<id>/` - Buscar dados de um evento
- `POST /deleteEvento/<id>/` - Excluir evento
- `GET /exportEventosExcel/` - Exportar eventos para Excel

### Tipos de Evento:
- `GET /gestaoTiposEvento/` - Página de gestão de tipos de evento
- `POST /addTipoEvento/` - Adicionar novo tipo de evento
- `POST /updateTipoEvento/<id>/` - Atualizar tipo de evento
- `GET /getTipoEvento/<id>/` - Buscar dados de um tipo de evento
- `POST /deleteTipoEvento/<id>/` - Excluir tipo de evento

## Modelos de Dados

### Evento
```python
class Evento(models.Model):
    tipo = models.ForeignKey(TipoEvento, on_delete=models.CASCADE)
    data = models.DateField('Data', null=True, blank=True)
    descricao = models.CharField('Descrição', max_length=50)
    Obs = models.TextField('Observação', max_length=250)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
```

### TipoEvento
```python
class TipoEvento(models.Model):
    tipo_evento = models.CharField('Tipo Evento', max_length=40)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
```

## Formulários

### EventoForm
- Validação automática dos campos obrigatórios
- Widgets customizados para melhor UX
- Integração com Bootstrap

### TipoEventoForm
- Validação de tamanho máximo
- Campo único para tipo de evento

## Segurança e Permissões

- **LoginRequiredMixin**: Todas as views requerem autenticação
- **AcessoAcoes**: Verificação de permissões por ação
- **CSRF Protection**: Proteção contra ataques CSRF
- **Validação de dados**: Validação tanto no frontend quanto backend

## Interface do Usuário

### Tecnologias Utilizadas:
- **Bootstrap 5**: Framework CSS para design responsivo
- **DataTables**: Plugin para tabelas interativas
- **Bootstrap Icons**: Ícones modernos
- **jQuery**: Manipulação do DOM e AJAX

### Características da Interface:
- **Design responsivo** para diferentes tamanhos de tela
- **Modais** para adição/edição sem recarregar a página
- **Filtros dinâmicos** com DataTables
- **Confirmações** para ações destrutivas
- **Feedback visual** para todas as operações

## Funcionalidades JavaScript

### Filtros Dinâmicos:
- Filtro por tipo de evento
- Filtro por período de data
- Busca por descrição
- Aplicação de múltiplos filtros simultaneamente

### Operações AJAX:
- Adição de eventos sem recarregar a página
- Edição inline via modais
- Exclusão com confirmação
- Busca de dados para edição

### Validações:
- Validação de campos obrigatórios
- Validação de formato de data
- Validação de tamanho máximo de campos

## Exportação de Dados

### Excel:
- Formatação profissional com cabeçalhos coloridos
- Ajuste automático de largura das colunas
- Nome do arquivo com timestamp
- Todos os dados relevantes incluídos

## Manutenção e Extensibilidade

### Código Organizado:
- Views separadas por funcionalidade
- Formulários reutilizáveis
- URLs bem estruturadas
- Templates modulares

### Possíveis Extensões:
- Integração com calendário
- Notificações por email
- Relatórios avançados
- Dashboard com estatísticas
- API REST para integração externa

## Instalação e Configuração

1. **Verificar dependências**:
   - Django
   - openpyxl (para exportação Excel)
   - django-widget-tweaks (para formulários)

2. **Configurar URLs**:
   - Adicionar as URLs do app RH ao urls.py principal

3. **Configurar permissões**:
   - Configurar as permissões no sistema de menus

4. **Criar tipos de evento iniciais**:
   - Acessar `/gestaoTiposEvento/` para criar tipos básicos

## Uso Recomendado

1. **Primeiro acesso**: Criar tipos de eventos básicos
2. **Uso diário**: Adicionar eventos conforme necessário
3. **Relatórios**: Usar exportação Excel para análises
4. **Manutenção**: Revisar e atualizar tipos de eventos periodicamente

## Suporte e Contato

Para dúvidas ou problemas com o sistema de gestão de eventos, entre em contato com a equipe de desenvolvimento. 