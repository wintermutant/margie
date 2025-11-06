from dataclasses import field
from uuid import UUID, uuid4

from pydantic_sqlite import DataBase
from pydantic import BaseModel, Field

class FastaRecord(BaseModel):
    uuid: UUID = Field(default_factory=uuid4, alias='uuid')
    description: str
    sequence: str

seq1 = FastaRecord(description="seq1", sequence="ATCG")
seq2 = FastaRecord(description="seq2", sequence="GGCTA")


db = DataBase("example2.db")
db.add('fasta_records', seq1)
db.add('fasta_records', seq2)

for x in db("fasta_records"):
    assert isinstance(x, FastaRecord)
    class_init = FastaRecord(**x.model_dump())
    print(class_init.sequence)

# db.save('example.db')
