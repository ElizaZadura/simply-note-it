#!/usr/bin/env python3
"""
Simply Note It - A simple text editor with split panels
Simplified version with better panel management
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys

class SimplyNoteIt:
    def __init__(self, root):
        self.root = root
        self.root.title("Simply Note It")
        self.root.geometry("1200x800")
        
        # Current file
        self.current_file = None
        self.text_changed = False
        
        # Split panel support
        self.split_mode = False
        self.panels = []
        self.current_panel = 0
        
        # Create menu bar
        self.create_menu()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create main text area
        self.create_text_area()
        
        # Create status bar
        self.create_status_bar()
        
        # Bind events
        self.bind_events()
        
        # Set initial focus
        self.text_area.focus_set()
    
    def create_menu(self):
        """Create the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        edit_menu.add_command(label="Find", command=self.find_text, accelerator="Ctrl+F")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Split Horizontal", command=self.split_horizontal, accelerator="Ctrl+Shift+H")
        view_menu.add_command(label="Split Vertical", command=self.split_vertical, accelerator="Ctrl+Shift+V")
        view_menu.add_command(label="Close Split", command=self.close_split, accelerator="Ctrl+Shift+W")
        view_menu.add_separator()
        view_menu.add_command(label="Next Panel", command=self.next_panel, accelerator="Ctrl+Tab")
        view_menu.add_command(label="Previous Panel", command=self.prev_panel, accelerator="Ctrl+Shift+Tab")
    
    def create_toolbar(self):
        """Create the toolbar"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        
        # Toolbar buttons
        ttk.Button(toolbar, text="New", command=self.new_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Open", command=self.open_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Save", command=self.save_file).pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Split buttons
        ttk.Button(toolbar, text="Split H", command=self.split_horizontal).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Split V", command=self.split_vertical).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Close Split", command=self.close_split).pack(side=tk.LEFT, padx=2)
        
        # Panel navigation
        ttk.Button(toolbar, text="Next Panel", command=self.next_panel).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Prev Panel", command=self.prev_panel).pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Font size
        ttk.Label(toolbar, text="Font Size:").pack(side=tk.LEFT, padx=2)
        self.font_size = tk.StringVar(value="12")
        font_combo = ttk.Combobox(toolbar, textvariable=self.font_size, width=5, values=["8", "9", "10", "11", "12", "14", "16", "18", "20", "24"])
        font_combo.pack(side=tk.LEFT, padx=2)
        font_combo.bind("<<ComboboxSelected>>", self.change_font_size)
    
    def create_text_area(self):
        """Create the main text area"""
        # Create frame for text area
        self.text_frame = ttk.Frame(self.root)
        self.text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create main text widget with scrollbar
        self.text_area = scrolledtext.ScrolledText(
            self.text_frame,
            wrap=tk.WORD,
            font=("Consolas", 12),
            undo=True,
            maxundo=50
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Configure text widget
        self.text_area.config(
            tabs=("2c", "4c", "6c", "8c"),  # Tab stops
            insertbackground="black",
            selectbackground="lightblue"
        )
        
        # Add to panels list
        self.panels = [self.text_area]
    
    def create_status_bar(self):
        """Create the status bar"""
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def bind_events(self):
        """Bind keyboard shortcuts and events"""
        # Keyboard shortcuts
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-Shift-S>", lambda e: self.save_as_file())
        self.root.bind("<Control-q>", lambda e: self.exit_app())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-x>", lambda e: self.cut())
        self.root.bind("<Control-c>", lambda e: self.copy())
        self.root.bind("<Control-v>", lambda e: self.paste())
        self.root.bind("<Control-a>", lambda e: self.select_all())
        self.root.bind("<Control-f>", lambda e: self.find_text())
        self.root.bind("<Control-Shift-H>", lambda e: self.split_horizontal())
        self.root.bind("<Control-Shift-V>", lambda e: self.split_vertical())
        self.root.bind("<Control-Shift-W>", lambda e: self.close_split())
        self.root.bind("<Control-Tab>", lambda e: self.next_panel())
        self.root.bind("<Control-Shift-Tab>", lambda e: self.prev_panel())
        
        # Text change detection
        self.text_area.bind("<KeyPress>", self.on_text_change)
        self.text_area.bind("<Button-1>", self.on_text_change)
        
        # Window close
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
    
    def on_text_change(self, event=None):
        """Handle text changes"""
        self.text_changed = True
        self.update_title()
        return "break"  # Don't interfere with the event
    
    def update_title(self):
        """Update window title with file status"""
        if self.current_file:
            filename = os.path.basename(self.current_file)
            status = "*" if self.text_changed else ""
            panel_info = f" (Panel {self.current_panel + 1}/{len(self.panels)})" if len(self.panels) > 1 else ""
            self.root.title(f"{filename}{status} - Simply Note It{panel_info}")
        else:
            status = "*" if self.text_changed else ""
            panel_info = f" (Panel {self.current_panel + 1}/{len(self.panels)})" if len(self.panels) > 1 else ""
            self.root.title(f"Untitled{status} - Simply Note It{panel_info}")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)
        self.root.after(3000, lambda: self.status_bar.config(text="Ready"))
    
    def get_current_panel(self):
        """Get the currently active panel"""
        if 0 <= self.current_panel < len(self.panels):
            return self.panels[self.current_panel]
        return self.text_area
    
    def focus_panel(self, panel_index):
        """Focus a specific panel"""
        if 0 <= panel_index < len(self.panels):
            self.current_panel = panel_index
            self.panels[panel_index].focus_set()
            self.update_title()
    
    def next_panel(self):
        """Switch to next panel"""
        if len(self.panels) > 1:
            self.current_panel = (self.current_panel + 1) % len(self.panels)
            self.focus_panel(self.current_panel)
            self.update_status(f"Switched to panel {self.current_panel + 1}")
    
    def prev_panel(self):
        """Switch to previous panel"""
        if len(self.panels) > 1:
            self.current_panel = (self.current_panel - 1) % len(self.panels)
            self.focus_panel(self.current_panel)
            self.update_status(f"Switched to panel {self.current_panel + 1}")
    
    # File operations
    def new_file(self):
        """Create a new file"""
        if self.text_changed:
            if messagebox.askyesno("Unsaved Changes", "Save current file?"):
                self.save_file()
        
        # Clear the current panel
        current_panel = self.get_current_panel()
        current_panel.delete(1.0, tk.END)
        
        self.current_file = None
        self.text_changed = False
        self.update_title()
        self.update_status("New file created")
    
    def open_file(self):
        """Open a file"""
        if self.text_changed:
            if messagebox.askyesno("Unsaved Changes", "Save current file?"):
                self.save_file()
        
        file_path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    current_panel = self.get_current_panel()
                    current_panel.delete(1.0, tk.END)
                    current_panel.insert(1.0, content)
                    self.current_file = file_path
                    self.text_changed = False
                    self.update_title()
                    self.update_status(f"Opened: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")
    
    def save_file(self):
        """Save current file"""
        if self.current_file:
            try:
                current_panel = self.get_current_panel()
                content = current_panel.get(1.0, tk.END)
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.text_changed = False
                self.update_title()
                self.update_status(f"Saved: {os.path.basename(self.current_file)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
        else:
            self.save_as_file()
    
    def save_as_file(self):
        """Save file with new name"""
        file_path = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                current_panel = self.get_current_panel()
                content = current_panel.get(1.0, tk.END)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.current_file = file_path
                self.text_changed = False
                self.update_title()
                self.update_status(f"Saved as: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
    
    def exit_app(self):
        """Exit the application"""
        if self.text_changed:
            if messagebox.askyesno("Unsaved Changes", "Save before exiting?"):
                self.save_file()
        self.root.quit()
    
    # Edit operations
    def undo(self):
        """Undo last action"""
        try:
            current_panel = self.get_current_panel()
            current_panel.edit_undo()
        except tk.TclError:
            pass
    
    def redo(self):
        """Redo last undone action"""
        try:
            current_panel = self.get_current_panel()
            current_panel.edit_redo()
        except tk.TclError:
            pass
    
    def cut(self):
        """Cut selected text"""
        current_panel = self.get_current_panel()
        current_panel.event_generate("<<Cut>>")
    
    def copy(self):
        """Copy selected text"""
        current_panel = self.get_current_panel()
        current_panel.event_generate("<<Copy>>")
    
    def paste(self):
        """Paste text"""
        current_panel = self.get_current_panel()
        current_panel.event_generate("<<Paste>>")
    
    def select_all(self):
        """Select all text"""
        current_panel = self.get_current_panel()
        current_panel.tag_add(tk.SEL, "1.0", tk.END)
        current_panel.mark_set(tk.INSERT, "1.0")
        current_panel.see(tk.INSERT)
    
    def find_text(self):
        """Find text dialog"""
        # Simple find dialog
        find_window = tk.Toplevel(self.root)
        find_window.title("Find")
        find_window.geometry("300x100")
        find_window.transient(self.root)
        find_window.grab_set()
        
        ttk.Label(find_window, text="Find:").pack(pady=5)
        find_entry = ttk.Entry(find_window, width=30)
        find_entry.pack(pady=5)
        find_entry.focus_set()
        
        def find():
            search_text = find_entry.get()
            if search_text:
                current_panel = self.get_current_panel()
                # Clear previous highlights
                current_panel.tag_remove("found", "1.0", tk.END)
                
                # Search for text
                start = "1.0"
                while True:
                    pos = current_panel.search(search_text, start, tk.END)
                    if not pos:
                        break
                    end = f"{pos}+{len(search_text)}c"
                    current_panel.tag_add("found", pos, end)
                    start = end
                
                # Configure highlight
                current_panel.tag_configure("found", background="yellow")
                
                # Move to first match
                first_match = current_panel.search(search_text, "1.0", tk.END)
                if first_match:
                    current_panel.see(first_match)
                    current_panel.mark_set(tk.INSERT, first_match)
        
        ttk.Button(find_window, text="Find", command=find).pack(pady=5)
        
        # Bind Enter key
        find_entry.bind("<Return>", lambda e: find())
    
    def change_font_size(self, event=None):
        """Change font size"""
        try:
            size = int(self.font_size.get())
            current_font = self.text_area.cget("font")
            font_family = current_font.split()[0] if current_font else "Consolas"
            # Apply to all panels
            for panel in self.panels:
                panel.config(font=(font_family, size))
        except ValueError:
            pass
    
    def split_horizontal(self):
        """Split the current panel horizontally"""
        if len(self.panels) >= 4:  # Limit to 4 panels
            messagebox.showinfo("Info", "Maximum of 4 panels allowed")
            return
        
        # Create new text widget
        new_text = scrolledtext.ScrolledText(
            self.text_frame,
            wrap=tk.WORD,
            font=("Consolas", 12),
            undo=True,
            maxundo=50
        )
        
        # Configure new text widget
        new_text.config(
            tabs=("2c", "4c", "6c", "8c"),
            insertbackground="black",
            selectbackground="lightblue"
        )
        
        # Bind events to new panel
        new_text.bind("<KeyPress>", self.on_text_change)
        new_text.bind("<Button-1>", self.on_text_change)
        
        # Add to panels list
        self.panels.append(new_text)
        
        # Reorganize layout
        self.reorganize_panels()
        
        # Focus the new panel
        self.current_panel = len(self.panels) - 1
        new_text.focus_set()
        
        self.split_mode = True
        self.update_title()
        self.update_status("Split horizontally")
    
    def split_vertical(self):
        """Split the current panel vertically"""
        if len(self.panels) >= 4:  # Limit to 4 panels
            messagebox.showinfo("Info", "Maximum of 4 panels allowed")
            return
        
        # Create new text widget
        new_text = scrolledtext.ScrolledText(
            self.text_frame,
            wrap=tk.WORD,
            font=("Consolas", 12),
            undo=True,
            maxundo=50
        )
        
        # Configure new text widget
        new_text.config(
            tabs=("2c", "4c", "6c", "8c"),
            insertbackground="black",
            selectbackground="lightblue"
        )
        
        # Bind events to new panel
        new_text.bind("<KeyPress>", self.on_text_change)
        new_text.bind("<Button-1>", self.on_text_change)
        
        # Add to panels list
        self.panels.append(new_text)
        
        # Reorganize layout
        self.reorganize_panels()
        
        # Focus the new panel
        self.current_panel = len(self.panels) - 1
        new_text.focus_set()
        
        self.split_mode = True
        self.update_title()
        self.update_status("Split vertically")
    
    def close_split(self):
        """Close the split and return to single panel"""
        if len(self.panels) <= 1:
            messagebox.showinfo("Info", "No split to close")
            return
        
        # Remove the current panel (except the main one)
        if self.current_panel > 0:
            panel_to_remove = self.panels[self.current_panel]
            self.panels.remove(panel_to_remove)
            panel_to_remove.destroy()
            
            # Adjust current panel index
            if self.current_panel >= len(self.panels):
                self.current_panel = len(self.panels) - 1
        
        # Reorganize layout
        self.reorganize_panels()
        
        # Focus the remaining panel
        self.focus_panel(self.current_panel)
        
        if len(self.panels) == 1:
            self.split_mode = False
        
        self.update_title()
        self.update_status("Split closed")
    
    def reorganize_panels(self):
        """Reorganize the layout of panels"""
        # Clear the text frame
        for widget in self.text_frame.winfo_children():
            widget.pack_forget()
        
        if len(self.panels) == 1:
            # Single panel
            self.panels[0].pack(fill=tk.BOTH, expand=True)
        elif len(self.panels) == 2:
            # Two panels side by side
            self.panels[0].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.panels[1].pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        elif len(self.panels) == 3:
            # Three panels: top, bottom-left, bottom-right
            top_frame = ttk.Frame(self.text_frame)
            bottom_frame = ttk.Frame(self.text_frame)
            top_frame.pack(fill=tk.BOTH, expand=True)
            bottom_frame.pack(fill=tk.BOTH, expand=True)
            
            self.panels[0].pack(in_=top_frame, fill=tk.BOTH, expand=True)
            self.panels[1].pack(in_=bottom_frame, side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.panels[2].pack(in_=bottom_frame, side=tk.RIGHT, fill=tk.BOTH, expand=True)
        elif len(self.panels) == 4:
            # Four panels in a 2x2 grid
            top_frame = ttk.Frame(self.text_frame)
            bottom_frame = ttk.Frame(self.text_frame)
            top_frame.pack(fill=tk.BOTH, expand=True)
            bottom_frame.pack(fill=tk.BOTH, expand=True)
            
            self.panels[0].pack(in_=top_frame, side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.panels[1].pack(in_=top_frame, side=tk.RIGHT, fill=tk.BOTH, expand=True)
            self.panels[2].pack(in_=bottom_frame, side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.panels[3].pack(in_=bottom_frame, side=tk.RIGHT, fill=tk.BOTH, expand=True)

def main():
    """Main function"""
    root = tk.Tk()
    app = SimplyNoteIt(root)
    root.mainloop()

if __name__ == "__main__":
    main()