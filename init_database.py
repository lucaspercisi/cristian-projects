"""
Script para inicializar o banco de dados com SQLAlchemy
"""
from app_new import create_app
from models import db, User, Permissao

def init_database():
    """Cria as tabelas e usuário admin inicial"""
    app = create_app()
    
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")
        
        # Verificar se já existe usuário admin
        admin = User.query.filter_by(usuario='admin').first()
        
        if not admin:
            # Criar usuário admin
            admin = User(
                usuario='admin',
                email='admin@sistema.com',
                ativo=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            print("✅ Usuário admin criado!")
            print("   Usuário: admin")
            print("   Senha: admin123")
            
            db.session.commit()
        else:
            print("⚠️  Usuário admin já existe")
        
        # Criar permissões básicas
        permissoes = [
            'administrador',
            'cadastrar_pessoas',
            'ver_financeiro',
            'editar_financeiro',
            'ver_relatorios',
            'gerenciar_usuarios'
        ]
        
        for perm_nome in permissoes:
            perm = Permissao.query.filter_by(nome=perm_nome).first()
            if not perm:
                perm = Permissao(
                    nome=perm_nome,
                    descricao=f'Permissão de {perm_nome}'
                )
                db.session.add(perm)
        
        if admin:
            # Adicionar todas as permissões ao admin
            for perm_nome in permissoes:
                perm = Permissao.query.filter_by(nome=perm_nome).first()
                if perm and perm not in admin.permissoes:
                    admin.permissoes.append(perm)
        
        db.session.commit()
        print("✅ Permissões criadas e atribuídas ao admin!")
        
        print("\n🎉 Banco de dados inicializado com sucesso!")

if __name__ == '__main__':
    init_database()

