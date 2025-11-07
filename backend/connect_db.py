from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Credenziali e info DB
DATABASE_URL = (
    "mysql+pymysql://4YT1j5qM7bVtKfh.root:Ou7RUXi9tQ5G61tN"
    "@gateway01.eu-central-1.prod.aws.tidbcloud.com:4000/anime_db"
    "?ssl_verify_identity=true&ssl_ca=C:/Users/m.spinelli/Workspace/drakk/watchlist/backend/isrgrootx1.pem"
)

# Crea il motore SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Crea sessioni
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
