"""Admin Dashboard and management workflows."""

from __future__ import annotations

import pygame as p
import bcrypt

from database.db import Database


class AdminPanel:
    """Admin panel with dashboard, user management, and game logs."""

    BG_COLOR = (40, 44, 52)
    PANEL_COLOR = (50, 54, 62)
    BUTTON_COLOR = (16, 185, 129)
    BUTTON_HOVER = (52, 211, 153)
    TEXT_COLOR = (255, 255, 255)
    TEXT_GRAY = (158, 158, 158)

    INPUT_COLOR = (60, 64, 72)
    INPUT_ACTIVE = (70, 74, 82)
    DANGER_COLOR = (220, 70, 70)
    DANGER_HOVER = (235, 92, 92)

    def __init__(self, width: int = 1180, height: int = 760):
        p.init()
        self.width = width
        self.height = height
        self.screen = p.display.set_mode((width, height))
        p.display.set_caption("Chess - Admin Dashboard")

        self.title_font = p.font.SysFont("Arial", 34, bold=True)
        self.header_font = p.font.SysFont("Arial", 24, bold=True)
        self.font = p.font.SysFont("Arial", 18)
        self.small_font = p.font.SysFont("Arial", 15)

        self.db = Database()
        self.clock = p.time.Clock()

        self.active_tab = "dashboard"  # dashboard | users | logs
        self.running = True
        self.message = ""
        self.message_color = self.TEXT_GRAY

        # User management state
        self.users = []
        self.selected_user = None
        self.modal = None  # None | create_user | edit_user | profile | confirm_delete
        self.modal_fields = {"username": "", "email": "", "password": ""}
        self.active_modal_field = None

        # Logs state
        self.games = []
        self.logs_user_filter = ""
        self.logs_sort_desc = True
        self.logs_filter_input_active = False

        # Shared rect stores for click handling
        self.tab_rects = {}
        self.user_action_rects = []
        self.modal_button_rects = {}
        self.logs_sort_rect = None
        self.logs_filter_rect = None
        self.back_button_rect = None
        self.create_user_rect = None

        self.refresh_data()

    def refresh_data(self):
        self.users = self.db.get_all_users()
        self.games = self.db.get_all_games(limit=500)

    def draw_button(self, rect, text, color=None, hover_color=None, text_color=None):
        color = color or self.BUTTON_COLOR
        hover_color = hover_color or self.BUTTON_HOVER
        text_color = text_color or self.TEXT_COLOR

        is_hover = rect.collidepoint(p.mouse.get_pos())
        p.draw.rect(self.screen, hover_color if is_hover else color, rect, border_radius=8)
        label = self.font.render(text, True, text_color)
        self.screen.blit(label, label.get_rect(center=rect.center))

    def draw_topbar(self):
        title = self.title_font.render("🛡 Admin Dashboard", True, self.BUTTON_COLOR)
        self.screen.blit(title, (24, 18))

        tabs = [
            ("dashboard", "Dashboard"),
            ("users", "User Management"),
            ("logs", "Game Logs"),
        ]

        start_x, y = 24, 76
        self.tab_rects = {}
        for key, text in tabs:
            rect = p.Rect(start_x, y, 220, 44)
            active = self.active_tab == key
            self.draw_button(
                rect,
                text,
                color=self.BUTTON_COLOR if active else self.PANEL_COLOR,
                hover_color=self.BUTTON_HOVER,
            )
            self.tab_rects[key] = rect
            start_x += 236

        self.back_button_rect = p.Rect(self.width - 170, 28, 140, 42)
        self.draw_button(self.back_button_rect, "Logout")

        if self.message:
            msg = self.small_font.render(self.message, True, self.message_color)
            self.screen.blit(msg, (24, 128))

    def draw_dashboard_tab(self):
        panel = p.Rect(24, 160, self.width - 48, self.height - 184)
        p.draw.rect(self.screen, self.PANEL_COLOR, panel, border_radius=12)

        total_users = len(self.users)
        total_games = self.db.get_total_games_count()

        card_w, card_h = 350, 130
        user_rect = p.Rect(80, 230, card_w, card_h)
        games_rect = p.Rect(470, 230, card_w, card_h)

        for rect, title, value in [
            (user_rect, "Total Users", str(total_users)),
            (games_rect, "Total Games Played", str(total_games)),
        ]:
            p.draw.rect(self.screen, self.BG_COLOR, rect, border_radius=10)
            label = self.header_font.render(title, True, self.TEXT_GRAY)
            num = self.title_font.render(value, True, self.TEXT_COLOR)
            self.screen.blit(label, (rect.x + 24, rect.y + 20))
            self.screen.blit(num, (rect.x + 24, rect.y + 62))

    def draw_users_tab(self):
        panel = p.Rect(24, 160, self.width - 48, self.height - 184)
        p.draw.rect(self.screen, self.PANEL_COLOR, panel, border_radius=12)

        self.create_user_rect = p.Rect(panel.right - 180, panel.y + 14, 156, 36)
        self.draw_button(self.create_user_rect, "Create User")

        headers = ["ID", "Username", "Email", "Created", "Last Login", "Actions"]
        widths = [70, 170, 260, 160, 180, 240]
        y0 = panel.y + 64
        x = panel.x + 16

        p.draw.rect(self.screen, self.BG_COLOR, (x, y0, panel.width - 32, 36), border_radius=8)
        for h, w in zip(headers, widths):
            self.screen.blit(self.small_font.render(h, True, self.TEXT_GRAY), (x + 8, y0 + 10))
            x += w

        self.user_action_rects = []
        y = y0 + 44
        for user in self.users[:9]:
            row_rect = p.Rect(panel.x + 16, y, panel.width - 32, 48)
            p.draw.rect(self.screen, self.BG_COLOR, row_rect, border_radius=8)

            created = (user.get("created_at") or "N/A").split(" ")[0]
            last_login = (user.get("last_login") or "Never").split(" ")[0]
            values = [
                str(user["user_id"]),
                user["username"],
                user["email"],
                created,
                last_login,
            ]

            x = panel.x + 26
            for idx, value in enumerate(values):
                surface = self.small_font.render(str(value), True, self.TEXT_COLOR if idx < 2 else self.TEXT_GRAY)
                self.screen.blit(surface, (x, y + 15))
                x += widths[idx]

            view_rect = p.Rect(x + 2, y + 8, 70, 30)
            edit_rect = p.Rect(x + 78, y + 8, 70, 30)
            delete_rect = p.Rect(x + 154, y + 8, 80, 30)
            self.draw_button(view_rect, "View")
            self.draw_button(edit_rect, "Edit")
            self.draw_button(delete_rect, "Delete", color=self.DANGER_COLOR, hover_color=self.DANGER_HOVER)

            self.user_action_rects.append((user, view_rect, edit_rect, delete_rect))
            y += 56

    def _filtered_sorted_games(self):
        filtered = self.games
        if self.logs_user_filter.strip():
            try:
                user_id = int(self.logs_user_filter.strip())
                filtered = [g for g in filtered if g.get("user_id") == user_id]
            except ValueError:
                filtered = []

        filtered.sort(key=lambda g: g.get("started_at") or "", reverse=self.logs_sort_desc)
        return filtered

    def draw_logs_tab(self):
        panel = p.Rect(24, 160, self.width - 48, self.height - 184)
        p.draw.rect(self.screen, self.PANEL_COLOR, panel, border_radius=12)

        self.logs_filter_rect = p.Rect(panel.x + 18, panel.y + 14, 220, 36)
        filter_color = self.INPUT_ACTIVE if self.logs_filter_input_active else self.INPUT_COLOR
        p.draw.rect(self.screen, filter_color, self.logs_filter_rect, border_radius=8)
        p.draw.rect(self.screen, self.BUTTON_COLOR, self.logs_filter_rect, 2, border_radius=8)

        filter_text = self.logs_user_filter if self.logs_user_filter else "Filter by User ID"
        filter_color_text = self.TEXT_COLOR if self.logs_user_filter else self.TEXT_GRAY
        self.screen.blit(self.small_font.render(filter_text, True, filter_color_text), (self.logs_filter_rect.x + 10, self.logs_filter_rect.y + 10))

        self.logs_sort_rect = p.Rect(panel.x + 252, panel.y + 14, 220, 36)
        sort_text = "Sort: Newest First" if self.logs_sort_desc else "Sort: Oldest First"
        self.draw_button(self.logs_sort_rect, sort_text)

        headers = ["Game ID", "Player 1", "Player 2", "Date", "Winner", "Moves"]
        widths = [100, 190, 190, 170, 170, 100]

        y0 = panel.y + 64
        x = panel.x + 16
        p.draw.rect(self.screen, self.BG_COLOR, (x, y0, panel.width - 32, 36), border_radius=8)

        for h, w in zip(headers, widths):
            self.screen.blit(self.small_font.render(h, True, self.TEXT_GRAY), (x + 8, y0 + 10))
            x += w

        games = self._filtered_sorted_games()
        y = y0 + 44
        for game in games[:10]:
            row_rect = p.Rect(panel.x + 16, y, panel.width - 32, 46)
            p.draw.rect(self.screen, self.BG_COLOR, row_rect, border_radius=8)

            player1 = game.get("username", "Unknown")
            player2 = "AI"
            result = (game.get("result") or "ongoing").lower()
            winner = {
                "win": player1,
                "loss": player2,
                "resign": player2,
                "draw": "Draw",
            }.get(result, "Ongoing")

            values = [
                game.get("game_id", "-"),
                player1,
                player2,
                (game.get("started_at") or "N/A").split(" ")[0],
                winner,
                game.get("total_moves", 0),
            ]

            x = panel.x + 26
            for idx, value in enumerate(values):
                color = self.TEXT_COLOR if idx in (0, 1, 4) else self.TEXT_GRAY
                self.screen.blit(self.small_font.render(str(value), True, color), (x, y + 14))
                x += widths[idx]

            y += 54

    def draw_modal(self):
        if not self.modal:
            return

        overlay = p.Surface((self.width, self.height), p.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        box = p.Rect(self.width // 2 - 240, self.height // 2 - 170, 480, 340)
        p.draw.rect(self.screen, self.PANEL_COLOR, box, border_radius=12)
        self.modal_button_rects = {}

        if self.modal in {"create_user", "edit_user"}:
            title = "Create User" if self.modal == "create_user" else "Edit User"
            self.screen.blit(self.header_font.render(title, True, self.TEXT_COLOR), (box.x + 20, box.y + 18))

            fields = ["username", "email", "password"]
            for idx, key in enumerate(fields):
                y = box.y + 70 + idx * 72
                label = "Password (optional)" if key == "password" and self.modal == "edit_user" else key.capitalize()
                self.screen.blit(self.small_font.render(label, True, self.TEXT_GRAY), (box.x + 22, y))

                rect = p.Rect(box.x + 22, y + 24, box.width - 44, 38)
                is_active = self.active_modal_field == key
                p.draw.rect(self.screen, self.INPUT_ACTIVE if is_active else self.INPUT_COLOR, rect, border_radius=8)
                p.draw.rect(self.screen, self.BUTTON_COLOR, rect, 2, border_radius=8)

                value = self.modal_fields[key]
                if key == "password" and value:
                    value = "•" * len(value)
                if not self.modal_fields[key] and key == "password" and self.modal == "edit_user":
                    value = "Leave blank to keep current password"
                color = self.TEXT_COLOR if self.modal_fields[key] else self.TEXT_GRAY
                self.screen.blit(self.small_font.render(value, True, color), (rect.x + 10, rect.y + 11))
                self.modal_button_rects[f"field_{key}"] = rect

            save_rect = p.Rect(box.x + 22, box.bottom - 56, 126, 36)
            cancel_rect = p.Rect(box.right - 148, box.bottom - 56, 126, 36)
            self.modal_button_rects["save"] = save_rect
            self.modal_button_rects["cancel"] = cancel_rect
            self.draw_button(save_rect, "Save")
            self.draw_button(cancel_rect, "Cancel", color=self.BG_COLOR, hover_color=self.INPUT_ACTIVE)

        elif self.modal == "profile":
            user = self.selected_user
            stats = self.db.get_user_stats(user["user_id"])
            self.screen.blit(self.header_font.render(f"Profile: {user['username']}", True, self.TEXT_COLOR), (box.x + 20, box.y + 20))

            lines = [
                f"User ID: {user['user_id']}",
                f"Email: {user['email']}",
                f"Created: {(user.get('created_at') or 'N/A').split(' ')[0]}",
                f"Last Login: {(user.get('last_login') or 'Never').split(' ')[0]}",
                f"Total Games: {stats.get('total_games', 0)}",
                f"Wins: {stats.get('wins', 0)} | Losses: {stats.get('losses', 0)} | Draws: {stats.get('draws', 0)}",
            ]
            for i, line in enumerate(lines):
                self.screen.blit(self.font.render(line, True, self.TEXT_GRAY), (box.x + 22, box.y + 70 + i * 38))

            close_rect = p.Rect(box.centerx - 70, box.bottom - 56, 140, 36)
            self.modal_button_rects["close"] = close_rect
            self.draw_button(close_rect, "Close")

        elif self.modal == "confirm_delete":
            user = self.selected_user
            self.screen.blit(self.header_font.render("Confirm Delete", True, self.DANGER_HOVER), (box.x + 20, box.y + 24))
            warning = f"Are you sure you want to delete '{user['username']}'?"
            sub = "This action cannot be undone."
            self.screen.blit(self.font.render(warning, True, self.TEXT_COLOR), (box.x + 20, box.y + 94))
            self.screen.blit(self.small_font.render(sub, True, self.TEXT_GRAY), (box.x + 20, box.y + 132))

            delete_rect = p.Rect(box.x + 22, box.bottom - 56, 160, 36)
            cancel_rect = p.Rect(box.right - 182, box.bottom - 56, 160, 36)
            self.modal_button_rects["confirm_delete"] = delete_rect
            self.modal_button_rects["cancel"] = cancel_rect
            self.draw_button(delete_rect, "Delete User", color=self.DANGER_COLOR, hover_color=self.DANGER_HOVER)
            self.draw_button(cancel_rect, "Cancel", color=self.BG_COLOR, hover_color=self.INPUT_ACTIVE)

    def open_create_modal(self):
        self.modal = "create_user"
        self.modal_fields = {"username": "", "email": "", "password": ""}
        self.active_modal_field = "username"

    def open_edit_modal(self, user):
        self.selected_user = user
        self.modal = "edit_user"
        self.modal_fields = {
            "username": user["username"],
            "email": user["email"],
            "password": "",
        }
        self.active_modal_field = "username"

    def save_user_modal(self):
        username = self.modal_fields["username"].strip()
        email = self.modal_fields["email"].strip()
        password = self.modal_fields["password"]

        if len(username) < 3:
            self.message, self.message_color = "Username must be at least 3 characters", self.DANGER_HOVER
            return
        if "@" not in email or "." not in email:
            self.message, self.message_color = "Please provide a valid email", self.DANGER_HOVER
            return

        if self.modal == "create_user":
            if len(password) < 6:
                self.message, self.message_color = "Password must be at least 6 characters", self.DANGER_HOVER
                return
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            user_id = self.db.create_user(username, email, hashed)
            if user_id:
                self.message, self.message_color = "User created successfully", self.BUTTON_COLOR
                self.modal = None
                self.refresh_data()
            else:
                self.message, self.message_color = "Username or email already exists", self.DANGER_HOVER
            return

        password_hash = None
        if password:
            if len(password) < 6:
                self.message, self.message_color = "Password must be at least 6 characters", self.DANGER_HOVER
                return
            password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        success, msg = self.db.update_user(self.selected_user["user_id"], username, email, password_hash)
        self.message, self.message_color = (msg, self.BUTTON_COLOR) if success else (msg, self.DANGER_HOVER)
        if success:
            self.modal = None
            self.refresh_data()

    def handle_modal_click(self, pos):
        for key, rect in self.modal_button_rects.items():
            if rect.collidepoint(pos):
                if key.startswith("field_"):
                    self.active_modal_field = key.replace("field_", "")
                    return
                if key in {"cancel", "close"}:
                    self.modal = None
                    self.active_modal_field = None
                    return
                if key == "save":
                    self.save_user_modal()
                    return
                if key == "confirm_delete":
                    if self.db.delete_user(self.selected_user["user_id"]):
                        self.message, self.message_color = "User deleted successfully", self.BUTTON_COLOR
                        self.refresh_data()
                    else:
                        self.message, self.message_color = "Failed to delete user", self.DANGER_HOVER
                    self.modal = None
                    return

    def handle_main_click(self, pos):
        if self.back_button_rect and self.back_button_rect.collidepoint(pos):
            self.running = False
            return

        for key, rect in self.tab_rects.items():
            if rect.collidepoint(pos):
                self.active_tab = key
                self.message = ""
                return

        if self.active_tab == "users":
            if self.create_user_rect and self.create_user_rect.collidepoint(pos):
                self.open_create_modal()
                return
            for user, view_rect, edit_rect, delete_rect in self.user_action_rects:
                if view_rect.collidepoint(pos):
                    self.selected_user = user
                    self.modal = "profile"
                    return
                if edit_rect.collidepoint(pos):
                    self.open_edit_modal(user)
                    return
                if delete_rect.collidepoint(pos):
                    self.selected_user = user
                    self.modal = "confirm_delete"
                    return

        if self.active_tab == "logs":
            if self.logs_filter_rect and self.logs_filter_rect.collidepoint(pos):
                self.logs_filter_input_active = True
            else:
                self.logs_filter_input_active = False

            if self.logs_sort_rect and self.logs_sort_rect.collidepoint(pos):
                self.logs_sort_desc = not self.logs_sort_desc

    def handle_keydown(self, event):
        if self.modal and self.active_modal_field:
            key = self.active_modal_field
            if event.key == p.K_BACKSPACE:
                self.modal_fields[key] = self.modal_fields[key][:-1]
            elif event.key == p.K_TAB:
                order = ["username", "email", "password"]
                idx = (order.index(key) + 1) % len(order)
                self.active_modal_field = order[idx]
            elif event.key == p.K_RETURN:
                self.save_user_modal()
            elif event.unicode and len(event.unicode) == 1 and event.unicode.isprintable():
                if len(self.modal_fields[key]) < 60:
                    self.modal_fields[key] += event.unicode
            return

        if self.active_tab == "logs" and self.logs_filter_input_active:
            if event.key == p.K_BACKSPACE:
                self.logs_user_filter = self.logs_user_filter[:-1]
            elif event.key == p.K_RETURN:
                self.logs_filter_input_active = False
            elif event.unicode and event.unicode.isdigit() and len(self.logs_user_filter) < 8:
                self.logs_user_filter += event.unicode

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.draw_topbar()

        if self.active_tab == "dashboard":
            self.draw_dashboard_tab()
        elif self.active_tab == "users":
            self.draw_users_tab()
        else:
            self.draw_logs_tab()

        self.draw_modal()
        p.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.running = False
                    return False
                if event.type == p.MOUSEBUTTONDOWN:
                    if self.modal:
                        self.handle_modal_click(event.pos)
                    else:
                        self.handle_main_click(event.pos)
                if event.type == p.KEYDOWN:
                    self.handle_keydown(event)

            self.draw()

        return True

    def close(self):
        self.db.close()


if __name__ == "__main__":
    admin = AdminPanel()
    admin.run()
    admin.close()
    p.quit()
