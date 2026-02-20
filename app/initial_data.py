from app.core.database import SessionLocal, engine
from app.models.role import Role

def init_db():
    db = SessionLocal()
    roles_to_create = ["farmer", "distributor", "admin"]
    
    for role_name in roles_to_create:
        existing_role = db.query(Role).filter(Role.name == role_name).first()
        if not existing_role:
            print(f"🌱 Creating role: {role_name}")
            new_role = Role(name=role_name, description=f"The {role_name} role")
            db.add(new_role)
        else:
            print(f"✅ Role already exists: {role_name}")
    
    db.commit()
    db.close()

if __name__ == "__main__":
    print("🚀 Initializing Database...")
    init_db()
    print("🏁 Done!")