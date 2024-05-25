## BudgetBuddy

BudgetBuddy é uma aplicação de gerenciamento de despesas projetada para ajudá-lo a manter o controle de seus gastos diários. Com esta aplicação, você pode facilmente adicionar, visualizar, editar e excluir despesas, garantindo uma gestão eficaz de suas finanças pessoais.

### Principais Recursos

- **Registro de Despesas**: Adicione facilmente suas despesas, incluindo data, descrição e valor.
- **Visualização Detalhada**: Visualize suas despesas em uma tabela fácil de entender, mostrando a data, descrição e valor de cada despesa.
- **Edição e Exclusão**: Edite ou exclua despesas existentes conforme necessário para manter seus registros atualizados.
- **Autenticação de Usuário**: A aplicação requer autenticação de usuário para garantir que apenas usuários autorizados possam acessar e gerenciar suas despesas.
- **Interface Amigável**: A interface intuitiva e amigável torna a navegação e o uso da aplicação simples e diretos.

### Tecnologias Utilizadas

- **Django**: Framework web utilizado para o desenvolvimento do back-end da aplicação.
- **HTML/CSS**: Utilizado para a estruturação e estilização das páginas web.
- **SQLite**: Banco de dados utilizado para armazenar os registros de despesas e informações do usuário.

### Instalação

Para executar o BudgetBuddy localmente, siga estas etapas:

1. Clone o repositório para o seu ambiente de desenvolvimento local:

   ```
   git clone https://github.com/seu-usuario/budgetbuddy.git
   ```

2. Navegue até o diretório do projeto:

   ```
   cd budgetbuddy
   ```

3. Instale as dependências do Python listadas no arquivo `requirements.txt`:

   ```
   pip install -r requirements.txt
   ```

4. Execute as migrações do banco de dados para criar as tabelas necessárias:

   ```
   python manage.py migrate
   ```

5. Inicie o servidor de desenvolvimento:

   ```
   python manage.py runserver
   ```

6. Acesse a aplicação em seu navegador da web usando o seguinte URL:

   ```
   http://localhost:8000
   ```

### Licença

Este projeto está licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT) - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Com o BudgetBuddy, gerenciar suas despesas nunca foi tão fácil! Se você tiver alguma dúvida ou precisar de assistência, não hesite em
