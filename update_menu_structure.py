"""
Script para atualizar a estrutura do menu sanduíche em todos os templates.
Move o menu sanduíche para fora do header, criando uma div separada.
"""

import os
import re

# Lista de arquivos para atualizar
templates_to_update = [
    'paginas/templates/painel/chat.html',
    'paginas/templates/painel/avisos.html',
    'paginas/templates/painel/comunicacao.html',
    'paginas/templates/painel/horarios_aula.html',
    'paginas/templates/painel/minhas_aulas.html',
    'paginas/templates/financeiro/mensalidades.html',
    'paginas/templates/financeiro/Extrato.html',
    'paginas/templates/financeiro/despesas.html',
    'paginas/templates/admin_painel/alunos.html',
    'paginas/templates/admin_painel/aulas.html',
    'paginas/templates/admin_painel/avisos.html',
    'paginas/templates/admin_painel/dashboard.html',
    'paginas/templates/admin_painel/eventos.html',
    'paginas/templates/admin_painel/mensalidades.html',
    'paginas/templates/admin_painel/professores.html',
    'paginas/templates/admin_painel/relatorio_financeiro.html',
    'paginas/templates/admin_painel/turmas.html',
    'paginas/templates/admin_painel/vendas_ingressos.html',
    'paginas/templates/admin_painel/mensagens.html',
    'paginas/templates/feedback/aba feedback.html',
    'paginas/templates/eventos/minhas_vendas.html',
    'paginas/templates/eventos/lista.html',
    'paginas/templates/eventos/detalhes.html',
    'paginas/templates/cadastros/cadastro_professor_novo.html',
    'paginas/templates/cadastros/cadastro_aluno_novo.html',
]

def update_template(file_path):
    """Atualiza um template movendo o menu sanduíche para fora do header"""
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se já está atualizado
    if '<!-- Menu Sanduíche - FORA do header -->' in content:
        print(f"⏭️  Já atualizado: {file_path}")
        return True
    
    # Padrão 1: Menu sanduíche dentro de sidebar-item no header
    pattern1 = r'(<div class="sidebar-item">.*?<button id="sidebar-toggle" class="menu-sanduiche".*?>.*?</button>.*?</div>)'
    
    # Encontrar o menu sanduíche
    match = re.search(pattern1, content, re.DOTALL)
    
    if not match:
        print(f"⚠️  Padrão não encontrado: {file_path}")
        return False
    
    menu_html = match.group(1)
    
    # Remover o menu do header
    content_without_menu = content.replace(menu_html, '')
    
    # Limpar espaços extras
    content_without_menu = re.sub(r'\n\s*\n\s*\n', '\n\n', content_without_menu)
    
    # Procurar pelo fechamento do header
    header_close_pattern = r'(</header>)'
    
    if not re.search(header_close_pattern, content_without_menu):
        print(f"⚠️  Tag </header> não encontrada: {file_path}")
        return False
    
    # Criar nova estrutura do menu
    new_menu_structure = '''
  <!-- Menu Sanduíche - FORA do header -->
  <div class="sidebar-item">
    <button id="sidebar-toggle" class="menu-sanduiche">
      <i class="bi bi-list"></i>
    </button>
  </div>
'''
    
    # Inserir o menu após o header
    new_content = re.sub(
        r'(</header>)',
        r'\1' + new_menu_structure,
        content_without_menu
    )
    
    # Salvar o arquivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Atualizado: {file_path}")
    return True

def main():
    print("🚀 Iniciando atualização dos templates...\n")
    
    success_count = 0
    error_count = 0
    
    for template_path in templates_to_update:
        try:
            if update_template(template_path):
                success_count += 1
            else:
                error_count += 1
        except Exception as e:
            print(f"❌ Erro ao processar {template_path}: {str(e)}")
            error_count += 1
    
    print(f"\n📊 Resumo:")
    print(f"✅ Sucesso: {success_count}")
    print(f"❌ Erros: {error_count}")
    print(f"📁 Total: {len(templates_to_update)}")

if __name__ == '__main__':
    main()
