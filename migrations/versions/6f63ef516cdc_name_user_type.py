"""name='user_type

Revision ID: 6f63ef516cdc
Revises: aba69a8bd25b
Create Date: 2020-11-11 22:26:17.846689

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f63ef516cdc'
down_revision = 'aba69a8bd25b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('email_address', sa.Column('active', sa.Boolean(), nullable=False))
    op.add_column('email_address', sa.Column('email_password', sa.String(length=255), nullable=False))
    op.add_column('email_address', sa.Column('last_mailbox_size', sa.Integer(), nullable=True))
    op.add_column('email_address', sa.Column('last_updated', sa.DateTime(), nullable=True))
    op.add_column('email_address', sa.Column('phishing_mail_detected', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('active', sa.Boolean(), nullable=False))
    op.add_column('user', sa.Column('last_logged_in', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('role', sa.Enum('USER', 'ADMIN', name='user_type'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'role')
    op.drop_column('user', 'last_logged_in')
    op.drop_column('user', 'active')
    op.drop_column('email_address', 'phishing_mail_detected')
    op.drop_column('email_address', 'last_updated')
    op.drop_column('email_address', 'last_mailbox_size')
    op.drop_column('email_address', 'email_password')
    op.drop_column('email_address', 'active')
    # ### end Alembic commands ###
