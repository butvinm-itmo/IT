from typing import Any, Dict, List, Type, TypeVar


class IncorrectAttrsSet(AttributeError):
    def __init__(self, cls_name: str, cls_fields: set[str], given_attrs: set[str], *args: object) -> None:
        msg = f'Invalid attributes: class {cls_name} must has fields {cls_fields} but {given_attrs} specified'
        super().__init__(msg, *args)


class FiledNotSpecifiedError(AttributeError):
    def __init__(self, cls_name: str, field_name: str, *args: object) -> None:
        msg = f'Field {field_name} must be specified for class {cls_name}'
        super().__init__(msg, *args)


class IncorrectSpecError(ValueError):
    def __init__(self, cls_name: str, field_name: str, field_spec: Any, given_value: Any, *args: object) -> None:
        msg = f'Field {field_name} of class {cls_name} must has value of {field_spec} but {given_value} taken'
        super().__init__(msg, *args)


T = TypeVar('T', bound='Element')


class Element:
    """Element is an atomic representation of some structure.
    It can contains attributes and children elements.
    Resolved types of children elements can be declared as new classes in element body 
    or specified at _children attribute

    """

    _children: List[Type['Element']]
    _fields: Dict[str, Any]
    _defaults: Dict[str, Any]
    _specs: Dict[str, Any]

    def __init__(self, attrs: Dict[str, Any], children_attrs: List[Dict[str, Any]]) -> None:
        """Check attrs set, if incorrect raise AttributeError.
        Check specificated fields, if incorrect raise ValueError. 
        Set attributes values and recursive initialize children by children_attrs
        """

        self._check_updating_attrs(attrs)
        self._check_specs(attrs)

    def __init_subclass__(cls: Any) -> None:
        """Find Element subclasses resolved in that class
        and update classes specified in __children attr. 
        Set _fields by annotation.

        Args:
            cls (Any): Subclass of Element
        """

        resolved_children = [
            attr for attr in cls.__dict__.values()
            if isinstance(attr, type) and issubclass(attr, Element)
        ]
        cls._children = getattr(cls, '_children', []) + resolved_children
        if '__annotations__' in cls.__dict__:
            cls._fields: Dict[str, Any] = cls.__annotations__
        else:
            cls._fields: Dict[str, Any] = {}

    @classmethod
    def specify(cls: Type[T], **kwargs: Any) -> Type[T]:
        """Make class with specified attributes values 

        Returns:
            _type_: Subclass of Element
        """

        cls._check_updating_attrs(kwargs)

        # pyright: reportGeneralTypeIssues=false
        cls_copy: Type[T] = type(
            cls.__name__, cls.__bases__, dict(cls.__dict__)
        )
        cls_copy._specs = kwargs
        return cls_copy

    @classmethod
    def _check_updating_attrs(cls, updating_attrs: Dict[str, Any]):
        """Check that updating_attrs is subset of cls._fields

        Args:
            updating_attrs (Dict[str, Any]): Attributes for updating

        Raises:
            IncorrectAttrsSet
        """

        cls_fields_names = set(cls._fields)
        updating_attrs_names = set(updating_attrs)
        if not cls_fields_names >= updating_attrs_names:
            raise IncorrectAttrsSet(
                cls.__name__, cls_fields_names, updating_attrs_names)

    @classmethod
    def _check_specs(cls, attrs: Dict[str, Any]):
        """Check if given attrs match with fields specifications

        Args:
            attrs (Dict[str, Any]): Given attributes
        
        Raises:
            FiledNotSpecifiedError
        """

        for field_name, field_spec in cls._fields.items():
            if field_name not in attrs:
                raise FiledNotSpecifiedError(cls.__name__, field_name)
            
            if attrs[field_name] != field_spec:
                raise IncorrectSpecError(cls.__name__, field_name, field_spec, attrs[field_name])
        