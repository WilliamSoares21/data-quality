# 📊 Dashboard de Qualidade de Dados

Bem-vindo ao repositório do **Dashboard de Qualidade de Dados**! 🚀 Este projeto foi desenvolvido com **Streamlit** para analisar e visualizar o desempenho de atendentes de forma intuitiva e interativa.

## ✨ Funcionalidades Principais

- 🔐 **Login de Usuário**
  - Autenticação com diferentes níveis de acesso (Administrador e Usuário Comum)
  - Armazenamento seguro de credenciais em variáveis de ambiente (em desenvolvimento)
- 👤 **Perfil do Usuário**
  - Exibição de avaliações individuais
  - Upload de foto de perfil
- 📈 **Gráficos de Desempenho**
  - Visualização de métricas semanais e mensais
  - Gráficos interativos com **Plotly**
- 🏆 **Ranking de Atendentes**
  - Exibição dos melhores atendentes com base nas avaliações
- ⚠️ **Denúncias**
  - Usuários podem registrar denúncias
  - Administradores podem visualizar e gerenciar as denúncias

## 🏗️ Melhorias Futuras

Atualmente, estou trabalhando para aprimorar diversas áreas do projeto, incluindo:
- 🎨 **Melhoria no Layout e Interface**
- 🔄 **Funcionalidade de Reset de Senha**
- 🆕 **Cadastro de Novo Usuário**
- ❓ **Opção "Esqueci Minha Senha"**
- 📧 **Vinculação com E-mail para recuperação de conta**
- 🔒 **Uso adequado de variáveis de ambiente** para proteger credenciais sensíveis

Se você tiver sugestões ou quiser colaborar, sinta-se à vontade para contribuir! 🚀

## 🏗️ Estrutura do Projeto
```
📂 app.py               # Arquivo principal
📂 data/                # Armazena dados, avaliações e denúncias
📂 pages/               # Contém scripts das páginas do app
  ├── admin/           # Páginas de Administrador
  │   ├── avaliacao.py 
  │   ├── denuncias.py 
  │   ├── graficos.py 
  │   ├── perfil.py 
  ├── usuario/         # Páginas de Usuário Comum
  │   ├── denuncias.py
  │   ├── ranking.py
📂 utils/               # Scripts utilitários
  ├── auth.py           # Autenticação
  ├── data.py           # Manipulação de dados (em desenvolvimento)
📂 .streamlit/
  ├── secrets.toml      # Configurações sensíveis (não versionado)
.gitignore              # Arquivos ignorados pelo Git
```

## 🚀 Como Configurar e Executar

### 📌 Configuração de Variáveis de Ambiente
Defina as variáveis de ambiente no seu sistema operacional para proteger informações sensíveis.

### 📦 Instalação
```bash
git clone https://github.com/seuusuario/dashboard-qualidade-dados.git
cd dashboard-qualidade-dados
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
```

### ▶️ Execução
```bash
streamlit run app.py
```

## ☁️ Implantação na Nuvem
O projeto pode ser facilmente implantado no **Streamlit Cloud**:
1. Acesse [Streamlit Cloud](https://share.streamlit.io/)
2. Faça login com sua conta do GitHub
3. Selecione este repositório
4. Configure as variáveis de ambiente
5. 🚀 Pronto!

## 📜 Licença
Este projeto está sob a **Licença MIT**, permitindo o uso, modificação e distribuição.

## 🤝 Contribuições
Ficarei feliz em receber contribuições! Se quiser ajudar a melhorar este projeto, sinta-se à vontade para abrir um **Pull Request** ou criar uma **Issue**.

💡 Qualquer sugestão ou feedback são bem-vindos! Vamos construir algo incrível juntos. 🚀

