"""change phishing mail FK to email_id, fixed typo

Revision ID: 85dcee72b6c4
Revises: 99ac5ea477fc
Create Date: 2020-11-11 22:48:36.159675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85dcee72b6c4'
down_revision = '99ac5ea477fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('phishing_email',
    sa.Column('mail_id', sa.Integer(), nullable=False),
    sa.Column('sender_address', sa.String(length=30), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('receiver_address', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['receiver_address'], ['email_address.email_id'], ),
    sa.PrimaryKeyConstraint('mail_id')
    )
    op.create_index(op.f('ix_phishing_email_created_at'), 'phishing_email', ['created_at'], unique=False)
    op.create_index(op.f('ix_phishing_email_receiver_address'), 'phishing_email', ['receiver_address'], unique=False)
    op.create_index(op.f('ix_phishing_email_sender_address'), 'phishing_email', ['sender_address'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_phishing_email_sender_address'), table_name='phishing_email')
    op.drop_index(op.f('ix_phishing_email_receiver_address'), table_name='phishing_email')
    op.drop_index(op.f('ix_phishing_email_created_at'), table_name='phishing_email')
    op.drop_table('phishing_email')
    # ### end Alembic commands ###
