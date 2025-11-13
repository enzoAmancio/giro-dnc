"""
Script para padronizar todos os sidebars dos templates
Substitui o sidebar inline por {% include 'includes/sidebar.html' %}
"""

import os
import re

# Diretório base dos templates
BASE_DIR = r'c:\Users\enzo\Desktop\gir-dnc\giro-dnc\paginas\templates'

# Mapeamento de templates para suas variáveis de contexto
TEMPLATE_CONTEXT = {
    # Painel
    'painel/index.html': {'section': 'painel', 'active': 'painel_index'},
    'painel/horarios.html': {'section': 'painel', 'active': 'painel_horarios'},
    'painel/avisos.html': {'section': 'painel', 'active': 'painel_avisos'},
    'painel/minhas_aulas.html': {'section': 'aulas', 'active': 'painel_minhas_aulas'},
    'painel/comunicacao.html': {'section': 'comunicacao', 'active': 'painel_comunicacao'},
    'painel/chat.html': {'section': 'comunicacao', 'active': 'painel_chat'},
    
    # Financeiro
    'financeiro/mensalidades.html': {'section': 'financeiro', 'active': 'financeiro_mensalidades'},
    'financeiro/Extrato.html': {'section': 'financeiro', 'active': 'financeiro_extrato'},
    'financeiro/despesas.html': {'section': 'financeiro', 'active': 'financeiro_despesas'},
    'financeiro/minhas_despesas.html': {'section': 'financeiro', 'active': 'financeiro_despesas'},
    'financeiro/criar_despesa.html': {'section': 'financeiro', 'active': 'financeiro_despesas'},
    'financeiro/editar_despesa.html': {'section': 'financeiro', 'active': 'financeiro_despesas'},
    
    # Eventos
    'eventos/lista.html': {'section': 'eventos', 'active': 'eventos_lista'},
    'eventos/detalhes.html': {'section': 'eventos', 'active': 'eventos_lista'},
    'eventos/minhas_vendas.html': {'section': 'eventos', 'active': 'minhas_vendas'},
    
    # Admin
    'admin_painel/dashboard.html': {'section': 'admin', 'active': 'admin_dashboard'},
    'admin_painel/alunos.html': {'section': 'admin', 'active': 'admin_alunos'},
    'admin_painel/turmas.html': {'section': 'admin', 'active': 'admin_turmas'},
    'admin_painel/aulas.html': {'section': 'admin', 'active': 'admin_aulas'},
    'admin_painel/frequencia.html': {'section': 'admin', 'active': 'admin_frequencia'},
    'admin_painel/mensalidades.html': {'section': 'admin', 'active': 'admin_mensalidades'},
    'admin_painel/eventos.html': {'section': 'admin', 'active': 'admin_eventos'},
    'admin_painel/avisos.html': {'section': 'admin', 'active': 'admin_avisos'},
    'admin_painel/detalhes_aluno.html': {'section': 'admin', 'active': 'admin_alunos'},
    'admin_painel/editar_aluno.html': {'section': 'admin', 'active': 'admin_alunos'},
}

def update_template(filepath, context_vars):
    """Atualiza um template substituindo o sidebar inline pelo include"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Padrão para encontrar o sidebar completo (de <aside até </aside>)
    # Inclui variações com e sem espaços
    sidebar_pattern = r'<aside class="gd-sidebar[^>]*>.*?</aside>'
    
    # Encontrar o sidebar
    match = re.search(sidebar_pattern, content, re.DOTALL)
    
    if not match:
        print(f"❌ Sidebar não encontrado em: {filepath}")
        return False
    
    # Criar o novo conteúdo do sidebar com variáveis de contexto
    new_sidebar = f'''<!-- Sidebar Padronizado -->
    {{% with sidebar_section='{context_vars['section']}' sidebar_active='{context_vars['active']}' %}}
      {{% include 'includes/sidebar.html' %}}
    {{% endwith %}}'''
    
    # Substituir o sidebar antigo pelo novo
    new_content = re.sub(sidebar_pattern, new_sidebar, content, flags=re.DOTALL)
    
    # Salvar o arquivo
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Atualizado: {filepath}")
    return True

def main():
    """Processa todos os templates"""
    updated = 0
    failed = 0
    
    print("=" * 70)
    print("PADRONIZAÇÃO DE SIDEBARS")
    print("=" * 70)
    
    for template_path, context in TEMPLATE_CONTEXT.items():
        full_path = os.path.join(BASE_DIR, template_path)
        
        if not os.path.exists(full_path):
            print(f"⚠️  Arquivo não existe: {full_path}")
            failed += 1
            continue
        
        if update_template(full_path, context):
            updated += 1
        else:
            failed += 1
    
    print("=" * 70)
    print(f"✅ Templates atualizados: {updated}")
    print(f"❌ Falhas: {failed}")
    print("=" * 70)

if __name__ == '__main__':
    main()
