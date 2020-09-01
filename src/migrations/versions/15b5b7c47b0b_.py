"""empty message

Revision ID: 15b5b7c47b0b
Revises: 
Create Date: 2020-09-01 21:38:12.382763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15b5b7c47b0b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('criticality',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('value')
    )
    op.create_table('permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('value')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('value')
    )
    op.create_table('status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('value')
    )
    op.create_table('role_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=False),
    sa.Column('last_name', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=200), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), server_default=sa.text('0'), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('organisation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=70), nullable=False),
    sa.Column('passcode', sa.Text(), nullable=False),
    sa.Column('location', sa.String(length=30), nullable=False),
    sa.Column('registered_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('registered_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['registered_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), server_default=sa.text('NULL'), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('organisation_id', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['organisation_id'], ['organisation.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['status.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_organisation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('organisation_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['organisation_id'], ['organisation.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('remarks', sa.Text(), server_default=sa.text('NULL'), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project_metrics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('pending_tasks', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('completed_tasks', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('on_hold_tasks', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('total_tasks', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), server_default=sa.text('NULL'), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('assigned_by', sa.Integer(), nullable=True),
    sa.Column('assigned_to', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('criticality_id', sa.Integer(), nullable=True),
    sa.Column('expected_completion_date', sa.DateTime(), sa.Computed('created_at + INTERVAL 3 DAY', persisted=True), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('actual_completion_date', sa.DateTime(), server_default=sa.text('NULL'), nullable=True),
    sa.ForeignKeyConstraint(['assigned_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['assigned_to'], ['user.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['criticality_id'], ['criticality.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['status.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('task_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('remarks', sa.Text(), server_default=sa.text('NULL'), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task_history')
    op.drop_table('task')
    op.drop_table('project_metrics')
    op.drop_table('project_history')
    op.drop_table('user_organisation')
    op.drop_table('project')
    op.drop_table('organisation')
    op.drop_table('user')
    op.drop_table('role_permission')
    op.drop_table('status')
    op.drop_table('role')
    op.drop_table('permission')
    op.drop_table('criticality')
    # ### end Alembic commands ###
