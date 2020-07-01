from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey,
                        Integer, String, Text, UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base


base = declarative_base()


class WindSpeed(base):
    __tablename__ = 'windspeed'
    timestamp = Column(DateTime, primary_key=True, nullable=False)
    field = Column(Integer, ForeignKey('field.id'),
                   primary_key=True, nullable=False)
    value = Column(Float)
    __table_args__ = (UniqueConstraint('field',
                                       'timestamp',
                                       name='UC_field_time'),)


class WindDirection(base):
    __tablename__ = 'winddirection'
    timestamp = Column(DateTime, primary_key=True, nullable=False)
    field = Column(Integer, ForeignKey('field.id'),
                   primary_key=True, nullable=False)
    value = Column(Integer)
    __table_args__ = (UniqueConstraint('field',
                                       'timestamp',
                                       name='UC_field_time'),)


class Visibility(base):
    __tablename__ = 'visibility'
    timestamp = Column(DateTime, primary_key=True, nullable=False)
    field = Column(Integer, ForeignKey('field.id'),
                   primary_key=True, nullable=False)
    value = Column(Float)
    __table_args__ = (UniqueConstraint('field',
                                       'timestamp',
                                       name='UC_field_time'),)


class Longitude(base):
    __tablename__ = 'longitude'
    timestamp = Column(DateTime, primary_key=True, nullable=False)
    field = Column(Integer, ForeignKey('field.id'),
                   primary_key=True, nullable=False)
    value = Column(Float)
    __table_args__ = (UniqueConstraint('field',
                                       'timestamp',
                                       name='UC_field_time'),)


class Latitude(base):
    __tablename__ = 'latitude'
    timestamp = Column(DateTime, primary_key=True, nullable=False)
    field = Column(Integer, ForeignKey('field.id'),
                   primary_key=True, nullable=False)
    value = Column(Float)
    __table_args__ = (UniqueConstraint('field',
                                       'timestamp',
                                       name='UC_field_time'),)

####################################################


class user(base):
    __tablename__ = 'user'
    id = Column(Integer,
                primary_key=True,
                nullable=False)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    is_superuser = Column(Boolean, nullable=False, default=False)
    memo = Column(Text, nullable=False, default='')
    __table_args__ = (UniqueConstraint('username', name='uc_username'),)


class field(base):
    __tablename__ = 'field'
    id = Column(Integer,
                primary_key=True,
                nullable=False)
    name = Column(String(50), nullable=False)
    alias = Column(String(50), nullable=False)
    iframe = Column(String(200),
                    nullable=False,
                    default='')


class sensor(base):
    __tablename__ = 'sensor'
    id = Column(Integer,
                primary_key=True,
                nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    df_name = Column(String(50), nullable=False, unique=True)
    alias = Column(String(50), nullable=False)
    unit = Column(String(50), default='')
    icon = Column(String(50), default='')
    bg_color = Column(String(50), default='bg-aqua')


class field_sensor(base):
    __tablename__ = 'field_sensor'
    id = Column(Integer,
                primary_key=True,
                nullable=False)
    field = Column(Integer,
                   ForeignKey('field.id'),
                   nullable=False)
    sensor = Column(Integer,
                    ForeignKey('sensor.id'),
                    nullable=False)
    df_name = Column(String(50), nullable=False)
    alias = Column(String(50), nullable=False)
    unit = Column(String(50), default='')
    icon = Column(String(50), default='')
    bg_color = Column(String(50), default='bg-aqua')
    alert_min = Column(Float, nullable=False, default=0)
    alert_max = Column(Float, nullable=False, default=0)
    __table_args__ = (UniqueConstraint('field',
                                       'df_name',
                                       name='UC_field_df_name'),)


class user_access(base):
    __tablename__ = 'user_access'
    id = Column(Integer,
                primary_key=True,
                nullable=False)
    user = Column(Integer,
                  ForeignKey('user.id'),
                  nullable=False)
    field = Column(Integer,
                   ForeignKey('field.id'),
                   nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
