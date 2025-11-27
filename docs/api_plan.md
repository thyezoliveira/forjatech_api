# Plano da API - ForjaTech (Estado Atual)

Este documento descreve o estado atual da API da ForjaTech, com base no código implementado.

## Modelos de Dados

### Orçamento (`models/orcamento.py`)

O modelo de dados para um orçamento é o seguinte:

-   `id`: Identificador único (Integer, PK)
-   `nomeEmpresa`: Nome da empresa do cliente (String)
-   `ramoEmpresa`: Ramo de atuação da empresa (String)
-   `emailContato`: Email de contato do cliente (String)
-   `telefone`: Telefone de contato (String, opcional)
-   `assunto`: Assunto da solicitação (String)
-   `descricaoDetalhada`: Descrição detalhada do projeto (Text)
-   `confirmado`: Flag para confirmar o orçamento (Boolean, default: `False`)
-   `prazo`: Prazo estimado para o projeto (String, opcional)

## Endpoints da API

### `POST /`

-   **Descrição:** Recebe os dados de um formulário, cria um novo orçamento no banco de dados e dispara um e-mail de notificação.
-   **Corpo da Requisição (JSON):**
    ```json
    {
        "nomeEmpresa": "Empresa Exemplo",
        "ramoEmpresa": "Tecnologia",
        "emailContato": "contato@exemplo.com",
        "telefone": "11999998888",
        "assunto": "Novo Site",
        "descricaoDetalhada": "Preciso de um site institucional moderno e responsivo."
    }
    ```
-   **Resposta (Sucesso):** `201 Created`
    ```json
    {
        "msg": "Orçamento recebido e salvo com sucesso!"
    }
    ```
-   **Integração:** Utiliza o `email_module.py` para notificar a equipe ou o cliente sobre o novo orçamento.

### `GET /orcamentos`

-   **Descrição:** Retorna uma página HTML (`index.html`) que lista todos os orçamentos cadastrados no banco de dados.
-   **Tipo de Resposta:** `text/html`
-   **Observação:** Este endpoint não é uma API RESTful tradicional que retorna JSON, mas sim uma página web para visualização interna.

### Módulo de E-mail (`email_module.py`)

-   **Funcionalidade:** Envio de e-mails transacionais.
-   **Gatilho:**
    1.  **Criação de Orçamento:** É acionado quando um novo orçamento é criado com sucesso através do endpoint `POST /`.
-   **Observação:** Este módulo não possui um endpoint público, sendo consumido internamente pela aplicação.
