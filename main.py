from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, Session, relationship
from sqlalchemy import inspect, select

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "conta_usuario"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    nome_completo = Column(String)
    endereco = relationship("Endereco", back_populates="usuario",
                            cascade="all, delete-orphan")

    def __repr__(self):
        return f"Usuario(id={self.id}, nome={self.nome}, nome_completo={
            self.nome_completo})"

class Endereco(Base):
    __tablename__ = "endereco"
    id = Column(Integer, primary_key=True)
    endereco_email = Column(String(30), nullable=False)
    usuario_id = Column(Integer, ForeignKey("conta_usuario.id"),
                        nullable=False)
    usuario = relationship("Usuario", back_populates="endereco")

    def __repr__(self):
        return f"Endereco(id={self.id}, endereco_email={self.endereco_email})"

engine = create_engine("sqlite://")

with Session(engine) as sessao:
    matheus = Usuario(nome='Matheus', nome_completo='Matheus Guilherme',
                      endereco=[Endereco(endereco_email=
                                         'matheuskdev@email.com')])

    guilherme = Usuario(nome='Guilherme', nome_completo='Guilherme Matheus',
                    endereco=[Endereco(endereco_email='guilherme@email.br')])

    julia = Usuario(nome='Julia', nome_completo='Julia Ellen')

    sessao.add_all([matheus, guilherme, julia])
    sessao.commit()

    consulta_usuario = select(Usuario).where(Usuario.nome.in_(["Matheus",
                                                               'Guilherme']))
    print('Recuperando usuários a partir de condição de filtragem')
    for usuario in sessao.scalars(consulta_usuario):
        print(usuario)

    consulta_endereco = select(Endereco).where(Endereco.usuario_id.in_([2]))
    print('\nRecuperando os endereços de email de Guilherme')
    for endereco in sessao.scalars(consulta_endereco):
        print(endereco)

    consulta_ordem = select(Usuario).order_by(Usuario.nome_completo.desc())
    print("\nRecuperando info de maneira ordenada")
    for resultado in sessao.scalars(consulta_ordem):
        print(resultado)

    consulta_juncao = select(Usuario.nome_completo, 
                             Endereco.endereco_email).join_from(Endereco,
                                                                Usuario)
    print("\n")
    for resultado in sessao.scalars(consulta_juncao):
        print(resultado)

    sessao.close()
