from messenger import db
from messenger import token_reg

for i in range(150):
	t=token_reg()
	db.session.add(t)

db.session.commit()