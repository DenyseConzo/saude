# Saúde Fácil · Easy Health

Protótipo mobile + PWA da **Saúde Fácil**, feito com [Flet](https://flet.dev), a partir do relatório
`SaudeFacil_Relatorio.docx`. Todos os dados são **fictícios (mock)** e a app funciona sem internet nem backend.

O logótipo (`logo.png`) é usado no onboarding, no cabeçalho, no assistente e no ícone da app
(`src/assets/`: `logo.png`, `logo_mark.png`, `logo_mark_white.png`, `icon.png`, `splash_android.png`).

## Funcionalidades

| Ecrã | O que faz |
|------|-----------|
| Onboarding | 3 passos de apresentação (pode "Saltar") |
| Início | Saudação no idioma escolhido, atalhos, botão SOS, próxima consulta, dicas de saúde, unidade mais próxima |
| Assistente "Fácil" | Chat com respostas por palavras-chave (febre/malária, diarreia/cólera, tosse/TB, HIV, gravidez, emergências) e sugestões rápidas |
| Verificar sintomas | Triagem por sintomas + duração + idade → nível de risco, possíveis causas e próxima ação |
| Unidades sanitárias | Pesquisa por nome/serviço, filtros (tipo, 24h), favoritos, detalhe com ligar e direções |
| Consultas (telemedicina) | Médicos, marcação (tipo, dia, horário), cancelar, chamada de vídeo simulada |
| Perfil | Ficha de saúde, idioma (PT, Changana, Macua, Sena, Ndau), texto grande, modo escuro, reiniciar demo |
| Emergência | Ligar 112 (emergência geral), 110 (Alô Vida), 119 (Polícia) e primeiros socorros |

## Executar

```bash
pip install flet[all]        # ou: uv sync
cd src
flet run                     # janela desktop
flet run --web               # no browser (PWA)
flet run --android           # no telemóvel com a app Flet (Android/iOS), via QR code
```

> Dica: no browser, use as ferramentas de programador em modo telemóvel (≈ 400×820) — a app limita-se a 520 px de largura.

## Testes

```bash
pip install pytest
python -m pytest
```

Cobrem o motor de triagem, o assistente, o armazenamento em memória (pesquisa, favoritos, marcações) e
um teste de fumo que constrói todos os ecrãs (claro/escuro, texto normal/grande) sem abrir janela.

## Estrutura

```
src/
  main.py              # ponto de entrada
  data/mock_data.py    # todos os dados fictícios
  services/            # lógica pura e testável
    triage.py          # regras de triagem
    assistant.py       # respostas do assistente (troca-se facilmente por uma IA real)
    store.py           # estado em memória: unidades, médicos, consultas
  ui/
    app.py             # navegação (separadores + pilha de ecrãs), tema, toasts
    theme.py, components.py
    screens/           # um ficheiro por ecrã
tests/
```

## Build

```bash
flet build web      # PWA (cores definidas em [tool.flet.web] no pyproject.toml)
flet build apk      # Android
flet build ipa      # iOS
```

⚠️ Protótipo informativo: não substitui avaliação médica.
"# SaudeFacil" 
