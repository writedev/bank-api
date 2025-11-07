# from sqlalchemy import event
# from sqlalchemy.orm import Session, UOWTransaction

# from core.db import engine
# from core.tables import BankAccount


# @event.listens_for(engine.sync_engine, "after_flush")
# def set_account_name(session: Session, flush_context: UOWTransaction):
#     for obj in session.new:
#         if isinstance(obj, BankAccount) and obj.name is None:
#             obj.name = f"{obj.owner_accounts.first_name}-{obj.owner_accounts.last_name}-{obj.id}"
