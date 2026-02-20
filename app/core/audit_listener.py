from sqlalchemy import event
from app.models.audit import AuditMixin
from app.core.context import get_current_user_id

# This function runs automatically whenever you save data
def register_audit_listeners():
    print("✅ Registering Audit Listeners...")

    @event.listens_for(AuditMixin, "before_insert", propagate=True)
    def set_created_by(mapper, connection, target):
        user_id = get_current_user_id()
        if user_id:
            target.created_by = user_id
            target.updated_by = user_id

    @event.listens_for(AuditMixin, "before_update", propagate=True)
    def set_updated_by(mapper, connection, target):
        user_id = get_current_user_id()
        if user_id:
            target.updated_by = user_id