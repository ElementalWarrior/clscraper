"""Set up posting models

Revision ID: 01c18d05df5f
Revises: 
Create Date: 2020-06-25 05:05:45.761880

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.types import BigInteger

# revision identifiers, used by Alembic.
revision = '01c18d05df5f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('postings',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('url', sa.Text(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('images', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('price', sa.DECIMAL(), nullable=True),
    sa.Column('price_currency', sa.String(length=10), nullable=True),
    sa.Column('floor_area', sa.Integer(), nullable=True),
    sa.Column('floor_area_units', sa.String(length=10), nullable=True),
    sa.Column('bedrooms', sa.Integer(), nullable=True),
    sa.Column('bathrooms', sa.Integer(), nullable=True),
    sa.Column('location', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('datetime_posted', sa.DateTime(), nullable=True),
    sa.Column('partial_scrape', sa.Boolean(), nullable=False),
    sa.Column('datetime_scraped', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posting_revisions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('posting_id', sa.BigInteger(), nullable=False),
    sa.Column('url', sa.Text(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('images', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('price', sa.DECIMAL(), nullable=True),
    sa.Column('price_currency', sa.String(length=10), nullable=True),
    sa.Column('floor_area', sa.Integer(), nullable=True),
    sa.Column('floor_area_units', sa.String(length=10), nullable=True),
    sa.Column('bedrooms', sa.Integer(), nullable=True),
    sa.Column('bathrooms', sa.Integer(), nullable=True),
    sa.Column('location', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('datetime_posted', sa.DateTime(), nullable=True),
    sa.Column('partial_scrape', sa.Boolean(), nullable=False),
    sa.Column('datetime_scraped', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['posting_id'], ['postings.id'], ),
    sa.PrimaryKeyConstraint('id', 'posting_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posting_revisions')
    op.drop_table('postings')
    # ### end Alembic commands ###
