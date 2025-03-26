from game.board import Board
import pytest
from game_session import GameSession
from game.move import Move
from game.piece import Piece
from game.piece_direction import PieceDirection
from game.team import Team

def test_empty_board_display_htmx():
    """Test that an empty board renders correctly with alternating light/dark squares."""
    board = Board()
    html = board.display_htmx()
    
    # Check that we have 64 spaces (8x8 grid)
    assert html.count('<div class="w-16 h-16') == 64
    
    # Check that we have alternating light/dark squares
    assert 'bg-board-light' in html
    assert 'bg-board-dark' in html
    
    # Check that each space has the correct data attributes
    assert 'data-row="0"' in html
    assert 'data-col="0"' in html
    assert 'data-selected="false"' in html


def test_board_with_pieces_display_htmx(white_piece, black_piece):
    """Test that pieces are rendered correctly with appropriate styling."""
    board = Board()
    
    # Place a white piece and a black piece
    board.board[0][0].add_piece(white_piece)
    board.board[1][1].add_piece(black_piece)
    
    html = board.display_htmx()
    
    # Check white piece styling
    assert 'bg-gray-100' in html  # White piece background
    assert 'border-white' in html  # White piece border
    
    # Check black piece styling
    assert 'bg-gray-900' in html  # Black piece background
    assert 'border-gray-800' in html  # Black piece border
    
    # Check piece dimensions
    assert 'w-12 h-12' in html  # Piece size
    assert 'w-8 h-8' in html  # Inner circle size


@pytest.fixture
def game_with_both_crowned_pieces():
    """Creates a game with both black and white crowned pieces for display testing."""
    game = GameSession()
    # Create a black crowned piece
    black_piece = Piece(direction=PieceDirection.BOTH, team=Team.BLACK)
    game.board.get_space(0, 1).add_piece(black_piece)
    # Create a white crowned piece
    white_piece = Piece(direction=PieceDirection.BOTH, team=Team.WHITE)
    game.board.get_space(0, 3).add_piece(white_piece)
    return game

def test_board_with_crowned_pieces_display_htmx(game_with_both_crowned_pieces):
    """Test that crowned pieces are rendered correctly with crown symbol and glow effect."""
    html = game_with_both_crowned_pieces.board.display_htmx()
    
    # Check for crowned piece styling
    assert 'animate-glow' in html  # Glow animation for crowned pieces
    assert '♔' in html  # Crown symbol
    
    # Check crown colors
    assert 'color: #FFD700' in html  # Gold color for black crowned pieces
    assert 'color: #FFA500' in html  # Orange color for white crowned pieces


def test_board_interactive_elements_display_htmx():
    """Test that the board has the correct interactive elements and styling."""
    board = Board()
    html = board.display_htmx()
    
    # Check for interactive elements
    assert 'cursor-pointer' in html
    assert 'select-none' in html
    assert 'transition-all' in html
    assert 'duration-200' in html
    assert 'ease-in-out' in html


def test_board_grid_layout_display_htmx():
    """Test that the board maintains the correct grid layout."""
    board = Board()
    html = board.display_htmx()
    
    # Check grid container
    assert 'grid grid-cols-8' in html
    assert 'gap-0' in html 