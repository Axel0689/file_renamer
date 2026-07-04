"""
Undo/Redo engine per le operazioni di rinomina.
"""

import os
from dataclasses import dataclass, field
from datetime import datetime

from PyQt5.QtCore import QObject, pyqtSignal


@dataclass
class RenameOperation:
    """Singola operazione atomica di rinomina."""

    old_path: str
    new_path: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class RenameTransaction:
    """Gruppo di operazioni eseguite insieme (un batch di rinomina)."""

    operations: list[RenameOperation]
    description: str = ""


class UndoStack(QObject):
    """
    Stack undo/redo per transazioni di rinomina.

    Segnali:
        can_undo_changed(bool)  — emesso quando cambia la disponibilita di undo
        can_redo_changed(bool)  — emesso quando cambia la disponibilita di redo
        status_message(str)     — messaggio da mostrare nella status bar
    """

    can_undo_changed = pyqtSignal(bool)
    can_redo_changed = pyqtSignal(bool)
    status_message = pyqtSignal(str)

    MAX_HISTORY = 50

    def __init__(self, parent=None):
        super().__init__(parent)
        self._undo_stack: list[RenameTransaction] = []
        self._redo_stack: list[RenameTransaction] = []

    # ---------------------------------------------------------------- Public
    def execute(self, transaction: RenameTransaction) -> list[str]:
        """
        Esegue tutte le rinomina della transazione.
        In caso di errore parziale, fa rollback delle operazioni gia completate.
        Restituisce lista di messaggi di errore (vuota se tutto OK).
        """
        completed: list[RenameOperation] = []
        errors = self._rename_operations(transaction.operations, completed)

        if errors and completed:
            rollback_operations = [
                RenameOperation(op.new_path, op.old_path) for op in reversed(completed)
            ]
            self._rename_operations(rollback_operations)
            return errors

        if not errors:
            # Successo: salva nello stack undo, svuota redo
            self._push_undo(transaction)
            self._redo_stack.clear()
            self._emit_signals()
            self.status_message.emit(f"Rinominati {len(completed)} file.")

        return errors

    def undo(self) -> bool:
        """Annulla l'ultima transazione. Restituisce True se riuscito."""
        if not self._undo_stack:
            return False

        transaction = self._undo_stack.pop()
        reversed_operations = [
            RenameOperation(old_path=op.new_path, new_path=op.old_path)
            for op in reversed(transaction.operations)
        ]
        errors = self._rename_operations(reversed_operations)

        if not errors:
            self._redo_stack.append(transaction)
            self.status_message.emit(f"Annullato: {transaction.description}")
        else:
            # Rimetti nello stack anche se parzialmente fallito
            self._undo_stack.append(transaction)

        self._emit_signals()
        return not bool(errors)

    def redo(self) -> bool:
        """Ripristina l'ultima transazione annullata. Restituisce True se riuscito."""
        if not self._redo_stack:
            return False

        transaction = self._redo_stack.pop()
        errors = self._rename_operations(transaction.operations)

        if not errors:
            self._push_undo(transaction)
            self.status_message.emit(f"Ripristinato: {transaction.description}")
        else:
            self._redo_stack.append(transaction)

        self._emit_signals()
        return not bool(errors)

    @property
    def can_undo(self) -> bool:
        return bool(self._undo_stack)

    @property
    def can_redo(self) -> bool:
        return bool(self._redo_stack)

    def history(self) -> list[str]:
        """Lista delle descrizioni delle transazioni nello stack undo."""
        return [tx.description for tx in self._undo_stack]

    # --------------------------------------------------------------- Private
    def _push_undo(self, transaction: RenameTransaction):
        self._undo_stack.append(transaction)
        if len(self._undo_stack) > self.MAX_HISTORY:
            self._undo_stack.pop(0)

    def _emit_signals(self):
        self.can_undo_changed.emit(self.can_undo)
        self.can_redo_changed.emit(self.can_redo)

    @staticmethod
    def _rename_operations(
        operations: list[RenameOperation],
        completed: list[RenameOperation] | None = None,
    ) -> list[str]:
        errors = []
        for operation in operations:
            try:
                os.rename(operation.old_path, operation.new_path)
                if completed is not None:
                    completed.append(operation)
            except OSError as error:
                filename = os.path.basename(operation.old_path)
                errors.append(f"{filename}: {error}")
        return errors
