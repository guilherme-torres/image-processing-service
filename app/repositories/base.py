from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from sqlmodel import Session, select


ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session

    
    def create(self, data: Dict[str, Any]) -> ModelType:
        obj = self.model(**data)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj
    

    def get(self, id: int) -> Optional[ModelType]:
        return self.session.get(self.model, id)
    

    def get_all(self, limit: int = 100, skip: int = 0) -> List[ModelType]:
        return self.session.exec(select(self.model).offset(skip).limit(limit)).all()
    

    def delete(self, id: int) -> bool:
        obj = self.get(id)
        if not obj:
            return False
        self.session.delete()
        self.session.commit()
        return True
    

    def update(self, id: int, data: Dict[str, Any]) -> Optional[ModelType]:
        obj = self.get(id)
        if not obj:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj
