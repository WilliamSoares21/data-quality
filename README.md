# 📊 Dashboard de Qualidade de Dados

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Security: OWASP Aligned](https://img.shields.io/badge/security-OWASP%20Aligned-green.svg)](https://owasp.org/)

> **Aplicação interativa de análise de desempenho, métricas de atendimento e gestão de qualidade de dados**, desenvolvida com foco em **Clean Architecture**, **Segurança da Informação (AppSec / OWASP)** e **UX reativa**.

Projetado como um projeto educacional de engenharia de software, o sistema opera no modo **Demonstração em Nuvem (Presentation Mode)**, garantindo persistência volátil e isolamento estrito por visitante através de `st.session_state` com mock data de alta fidelidade, sem custos de infraestrutura e com imunidade total contra contaminação de dados por terceiros.

---

## 🌐 Acesso à Demonstração (Live Demo)

Para testar todos os fluxos e níveis de acesso da aplicação na nuvem:

### 🔗 [Acessar Demonstração Online no Streamlit Cloud](https://data-quality.streamlit.app/)

### 🔑 Credenciais para Avaliação

| Perfil | Usuário | Senha | Nível de Acesso | Funcionalidades Habilitadas |
| --- | --- | --- | --- | --- |
| **Administrador** | `admin` | `admin123` | **Total (`admin`)** | 📝 Avaliação de Atendentes<br>📈 Gráficos Semanais/Mensais (Plotly)<br>🛡️ Moderação de Denúncias<br>👤 Perfil e Ranking |
| **Usuário Geral** | `user` | `user123` | **Restrito (`user`)** | 👤 Perfil do Usuário e Upload de Foto<br>⚠️ Registro de Denúncias<br>🏆 Ranking Público da Equipe |

> [!NOTE]
> **Segurança de Autenticação (OWASP A02 & A07)**:
> As senhas informadas são verificadas em tempo de execução contra hashes criptográficos derivados com **Argon2id** (gerenciados via `passlib`). Nenhuma credencial em texto claro é armazenada no código-fonte.

---

## 🏛️ Decisões de Arquitetura e Engenharia

1. **Roteamento Moderno e Declarativo**:
   - Utilização das APIs nativas `st.Page` e `st.navigation`, eliminando a necessidade de múltiplos scripts isolados na pasta `pages/` e centralizando o controle de sessão no ponto de entrada.

2. **Separação em Camadas Limpas (Clean Architecture)**:
   - **Camada de Apresentação (`views/`)**: Telas desacopladas que apenas renderizam componentes e consomem contratos de serviço.
   - **Camada de Repositório (`database/repository.py`)**: Centraliza as operações CRUD e regras de negócio sobre os dados.
   - **Camada de Segurança e Autenticação (`utils/auth.py`, `utils/security.py`)**: Guardas de autorização, sanitização e hashing.

3. **Modo Demonstração com Isolamento por Sessão**:
   - Cada visitante recebe uma instância isolada em memória (`st.session_state`) populada automaticamente com histórico temporal de avaliações, métricas e avatares padrão.
   - Ações realizadas (inserir avaliações, registrar denúncias, atualizar foto) afetam exclusivamente a sessão ativa do visitante.
   - Inclui botão de **"Restaurar Dados Demo"** na barra lateral para redefinir o estado a qualquer momento.

---

## 🛡️ Práticas de Segurança da Informação (AppSec)

| Vulnerabilidade / Prática | Implementação no Projeto |
| --- | --- |
| **Controle de Acesso Quebrado (OWASP A01)** | Guarda declarativo [`check_permission`] no topo de cada visão restrita, interrompendo a execução com `st.stop()` em acessos não autorizados. |
| **Falhas Criptográficas (OWASP A02)** | Hashing com algoritmo resistente a GPU/ASIC **Argon2id** (`argon2-cffi` / `passlib`) com salt automático. |
| **Prevenção contra Injeção (OWASP A03)** | Ausência de interpolação SQL/NoSQL no modo de demonstração em memória. |
| **Proteção de Segredos** | Credenciais sensíveis isoladas no `secrets.toml`, devidamente registrado no [`.gitignore`] e fornecido via modelo [`.streamlit/secrets.toml.example`]. |
| **Mitigação de Path Traversal** | Sanitização rigorosa de nomes de arquivos com `werkzeug.utils.secure_filename` e validação de MIME types de imagens via `Pillow`. |

---

## 📂 Estrutura do Repositório

```
data-quality/
├── .devcontainer/               # Configuração de ambiente reproduzível
├── .streamlit/
│   └── secrets.toml.example     # Modelo seguro de segredos (RBAC + Argon2id)
├── database/
│   ├── connection.py            # Provedor de dados e inicialização de sessão
│   └── repository.py            # Operações CRUD e Mock Data em memória
├── tests/
│   └── test_refactoring.py      # Suíte de testes unitários (RBAC, AppSec, CRUD)
├── utils/
│   ├── auth.py                  # Autenticação, Hashing Argon2id e Guarda RBAC
│   └── security.py              # Sanitização de Path Traversal e validação de uploads
├── views/
│   ├── login.py                 # Formulário de login
│   ├── perfil.py                # Perfil do colaborador e upload de foto
│   ├── user_denuncias.py        # Registro de denúncias
│   ├── user_ranking.py          # Ranking comparativo de desempenho
│   ├── admin_avaliacao.py       # Lançamento de notas por critérios (Admin)
│   ├── admin_graficos.py        # Análise temporal semanal/mensal com Plotly (Admin)
│   └── admin_denuncias.py       # Painel de moderação e análise de denúncias (Admin)
├── .gitignore                   # Proteção de arquivos sensíveis e caches
├── app.py                       # Ponto de entrada, roteador e configuração global
├── LICENSE                      # Licença MIT
├── README.md                    # Apresentação do projeto e documentação
└── requirements.txt             # Dependências essenciais da aplicação
```

---

## 💻 Como Reproduzir o Projeto Localmente

Caso queira clonar e inspecionar o código em sua própria máquina:

```bash
# 1. Clonar o repositório
git clone https://github.com/WilliamSoares21/data-quality.git
cd data-quality

# 2. Criar e ativar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Criar arquivo de credenciais local
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# 5. Executar os testes unitários
python -m unittest discover -s tests -p "test_*.py"

# 6. Executar o dashboard
streamlit run app.py
```

---

## 🧪 Testes Automatizados

O projeto conta com suíte de testes unitários automatizados validando:

- Sanitização contra ataques de *Path Traversal*;
- Hashing e verificação de senhas com *Argon2id*;
- Bloqueio de acesso por perfil na guarda RBAC (*check_permission*);
- Ciclo de vida completo das operações CRUD em memória (avaliações, denúncias, fotos e reset de estado).

---

## 📜 Licença

Distribuído sob a licença **MIT**. Veja [`LICENSE`](LICENSE) para mais informações.
