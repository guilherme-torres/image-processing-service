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
    

    def get_all(self, limit: int = 100, skip: int = 0, filter_by: Optional[dict] = None) -> List[ModelType]:
        query = select(self.model)
        if filter_by is not None:
            for key, value in filter_by.items():
                query = query.where(getattr(self.model, key) == value)
        query = query.offset(skip).limit(limit)
        return self.session.exec(query).all()
    

    def delete(self, id: int) -> bool:
        obj = self.get(id)
        if not obj:
            return False
        self.session.delete(obj)
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
