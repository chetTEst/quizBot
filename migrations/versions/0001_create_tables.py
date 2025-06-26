"""initial tables

Revision ID: 0001
Revises: 
Create Date: 2025-06-26 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'quiz',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('short_code', sa.String(length=8), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('short_code'),
    )
    op.create_index(op.f('ix_quiz_short_code'), 'quiz', ['short_code'], unique=True)

    op.create_table(
        'question',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('quiz_id', sa.Integer(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('qtype', sa.Enum('tf', 'single', 'text', 'numeric', name='qtype'), nullable=False),
        sa.Column('time_limit', sa.Integer(), nullable=True),
        sa.Column('media_url', sa.String(length=255), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_question_quiz_id'), 'question', ['quiz_id'], unique=False)

    op.create_table(
        'choice',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('text', sa.String(length=255), nullable=True),
        sa.Column('is_correct', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_choice_question_id'), 'choice', ['question_id'], unique=False)

    op.create_table(
        'participant',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('quiz_id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.String(length=36), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_id')
    )
    op.create_index(op.f('ix_participant_quiz_id'), 'participant', ['quiz_id'], unique=False)

    op.create_table(
        'answer',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('participant_id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('value', sa.Text(), nullable=True),
        sa.Column('correct', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ),
        sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_answer_participant_id'), 'answer', ['participant_id'], unique=False)
    op.create_index(op.f('ix_answer_question_id'), 'answer', ['question_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_answer_question_id'), table_name='answer')
    op.drop_index(op.f('ix_answer_participant_id'), table_name='answer')
    op.drop_table('answer')
    op.drop_index(op.f('ix_participant_quiz_id'), table_name='participant')
    op.drop_table('participant')
    op.drop_index(op.f('ix_choice_question_id'), table_name='choice')
    op.drop_table('choice')
    op.drop_index(op.f('ix_question_quiz_id'), table_name='question')
    op.drop_table('question')
    op.drop_index(op.f('ix_quiz_short_code'), table_name='quiz')
    op.drop_table('quiz')
