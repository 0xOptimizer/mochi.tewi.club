from datetime import datetime
from ..main import db
import random
import hashlib
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, Text, Enum, BigInteger, TIMESTAMP

class ApiKey(db.Model):
    __tablename__ = 'api_keys'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    key = Column(String(255), nullable=False, unique=True)
    created_by = Column(String(255), nullable=True)
    level = Column(Integer, nullable=False, default=0)
    ignore_limits = Column(Boolean, nullable=False, default=False)
    name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    ip_addresses = Column(Text, nullable=True)
    status = Column(Enum('active', 'expired', 'revoked', 'suspended', name='status'), nullable=False, default='active')
    permission = Column(String(255), nullable=True)
    date_expiration = Column(String(255), nullable=True)
    date_created = Column(String(255), nullable=True)
    date_activation = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    @staticmethod
    def generate_key():
        rabbit_breeds = [
            "american_bunny", "angora_rabbit", "belgian_hare", "beveren_bunny", "britannia_petite_bunny", "bunnicula", "californian_bunny",
            "champagne_d_argent_rabbit", "checkered_giant", "cinnamon_bunny", "cretan_rabbit", "crossbreed_bunny", "ringo", "dutch_rabbit",
            "dwarf_hotot_bunny", "english_l_spot_bunny", "english_spot_rabbit", "fauve_de_bourgogne_bunny", "reisen", "florida_white_rabbit",
            "german_angora_bunny", "giant_angora_rabbit", "giant_chinchilla_bunny", "golden_rabbit", "harlequin_bunny", "havana_rabbit",
            "himalayan_bunny", "japanese_bunny", "lilac_rabbit", "seiran", "udongein"
            "lionhead_bunny", "mad_hatter_rabbit", "mini_lop_rabbit", "mini_rex_bunny", "mopsy",
            "netherland_dwarf_bunny", "nehelenia", "new_zealand_rabbit", "peter_rabbit", "polish_bunny", "rex_rabbit", "rhinelander_bunny",
            "sable_rabbit", "silver_rabbit", "silver_marten_bunny", "standard_chinchilla_rabbit", "tan_bunny",
            "thrianta_rabbit", "thumper", "vienna_bunny", "white_rabbit", "yummy_bunny"
        ]

        while True:
            key = hashlib.md5(str(random.getrandbits(128)).encode('utf-8')).hexdigest()
            random.shuffle(rabbit_breeds)
            suffix = rabbit_breeds[0]

            api_key = f'tewi-{key[:8]}-{key[8:12]}-{key[12:16]}-{key[16:]}-{suffix.lower()}'

            if not ApiKey.key_exists(api_key):
                return api_key

    @staticmethod
    def key_exists(key):
        return ApiKey.query.filter_by(key=key).first() is not None

    @staticmethod
    def insert_key(data):
        if 'key' not in data or not data['key']:
            data['key'] = ApiKey.generate_key()

        if 'date_created' not in data:
            data['date_created'] = datetime.now()

        new_key = ApiKey(**data)
        db.session.add(new_key)
        db.session.commit()
        return new_key
