from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
	"postgresql://tester:test_password@localhost:5432/lyrics",
	isolation_level="READ UNCOMMITTED"
)

conn = engine.connect()

Session = sessionmaker(bind=engine)

session = Session()
