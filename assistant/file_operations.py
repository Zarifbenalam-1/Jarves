#!/usr/bin/env python3
"""
file_operations.py
Advanced File Operations Module for JARVIS-X

This module handles all file and directory operations for JARVIS, including:
- File creation, reading, writing, deletion
- Directory management and organization
- Project structure generation
- File system navigation and analysis
- Smart file organization by type
- Batch file operations

Author: JARVIS-X Development Team
Version: 1.0.0
"""

import os
import shutil
import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import mimetypes
import hashlib

class FileOperationsManager:
    """
    Advanced file operations manager for JARVIS-X
    Handles all file system interactions with enhanced capabilities
    """
    
    def __init__(self):
        self.supported_encodings = ['utf-8', 'utf-16', 'ascii', 'latin-1']
        self.file_type_mappings = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.md', '.rst'],
            'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
            'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
            'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.php', '.rb', '.go', '.rs'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
            'data': ['.json', '.xml', '.csv', '.yaml', '.yml', '.sql', '.db', '.sqlite'],
            'fonts': ['.ttf', '.otf', '.woff', '.woff2', '.eot'],
            'executables': ['.exe', '.msi', '.deb', '.rpm', '.dmg', '.app'],
            'config': ['.ini', '.cfg', '.conf', '.properties', '.toml']
        }
        
    def create_file(self, filepath: str, content: str = "", encoding: str = 'utf-8') -> Dict[str, str]:
        """
        Create a file with optional content
        
        Args:
            filepath: Path where the file should be created
            content: Content to write to the file
            encoding: File encoding (default: utf-8)
            
        Returns:
            Dict with status and message
        """
        try:
            # Convert to Path object for better handling
            file_path = Path(filepath)
            
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create the file
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            # Get file info
            file_size = file_path.stat().st_size
            created_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return {
                'status': 'success',
                'message': f"✅ File created successfully: {filepath}",
                'details': {
                    'path': str(file_path.absolute()),
                    'size': f"{file_size} bytes",
                    'created': created_time,
                    'encoding': encoding
                }
            }
            
        except PermissionError:
            return {
                'status': 'error',
                'message': f"❌ Permission denied: Cannot create file at {filepath}",
                'details': {'error_type': 'PermissionError'}
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f"❌ Error creating file: {str(e)}",
                'details': {'error_type': type(e).__name__}
            }
    
    def write_file(self, filepath: str, content: str, mode: str = 'w', encoding: str = 'utf-8') -> Dict[str, str]:
        """
        Write content to a file (supports append mode)
        
        Args:
            filepath: Path to the file
            content: Content to write
            mode: Write mode ('w' for overwrite, 'a' for append)
            encoding: File encoding
            
        Returns:
            Dict with status and message
        """
        try:
            file_path = Path(filepath)
            
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, mode, encoding=encoding) as f:
                f.write(content)
            
            file_size = file_path.stat().st_size
            action = "appended to" if mode == 'a' else "written to"
            
            return {
                'status': 'success',
                'message': f"✅ Content {action} file: {filepath}",
                'details': {
                    'path': str(file_path.absolute()),
                    'size': f"{file_size} bytes",
                    'mode': mode
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f"❌ Error writing to file: {str(e)}",
                'details': {'error_type': type(e).__name__}
            }
    
    def read_file(self, filepath: str, max_size: int = 10485760) -> Dict[str, str]:  # 10MB limit
        """
        Read file contents with smart encoding detection
        
        Args:
            filepath: Path to the file to read
            max_size: Maximum file size to read (default: 10MB)
            
        Returns:
            Dict with status, message, and content
        """
        try:
            file_path = Path(filepath)
            
            if not file_path.exists():
                return {
                    'status': 'error',
                    'message': f"❌ File not found: {filepath}",
                    'details': {'error_type': 'FileNotFoundError'}
                }
            
            # Check file size
            file_size = file_path.stat().st_size
            if file_size > max_size:
                return {
                    'status': 'error',
                    'message': f"❌ File too large: {file_size} bytes (max: {max_size} bytes)",
                    'details': {'file_size': file_size, 'max_size': max_size}
                }
            
            # Try to read with different encodings
            content = None
            used_encoding = None
            
            for encoding in self.supported_encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    used_encoding = encoding
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                # Try binary mode for non-text files
                with open(file_path, 'rb') as f:
                    binary_content = f.read()
                return {
                    'status': 'partial',
                    'message': f"⚠️ Binary file detected: {filepath}",
                    'content': f"[Binary file - {file_size} bytes]",
                    'details': {
                        'is_binary': True,
                        'size': file_size,
                        'mime_type': mimetypes.guess_type(filepath)[0]
                    }
                }
            
            # Truncate very long content for display
            if len(content) > 5000:
                display_content = content[:5000] + f"\n... [Content truncated - file has {len(content)} characters]"
            else:
                display_content = content
            
            return {
                'status': 'success',
                'message': f"📄 Content of {filepath}:",
                'content': display_content,
                'details': {
                    'path': str(file_path.absolute()),
                    'size': f"{file_size} bytes",
                    'encoding': used_encoding,
                    'lines': len(content.splitlines()),
                    'characters': len(content)
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f"❌ Error reading file: {str(e)}",
                'details': {'error_type': type(e).__name__}
            }
    
    def delete_file(self, filepath: str) -> Dict[str, str]:
        """
        Delete a file with confirmation
        
        Args:
            filepath: Path to the file to delete
            
        Returns:
            Dict with status and message
        """
        try:
            file_path = Path(filepath)
            
            if not file_path.exists():
                return {
                    'status': 'error',
                    'message': f"❌ File not found: {filepath}",
                    'details': {'error_type': 'FileNotFoundError'}
                }
            
            if file_path.is_dir():
                return {
                    'status': 'error',
                    'message': f"❌ Path is a directory, not a file: {filepath}",
                    'details': {'error_type': 'IsADirectoryError'}
                }
            
            # Get file info before deletion
            file_size = file_path.stat().st_size
            
            # Delete the file
            file_path.unlink()
            
            return {
                'status': 'success',
                'message': f"✅ File deleted successfully: {filepath}",
                'details': {
                    'deleted_size': f"{file_size} bytes",
                    'deleted_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f"❌ Error deleting file: {str(e)}",
                'details': {'error_type': type(e).__name__}
            }
    
    def list_directory(self, path: str = ".", detailed: bool = False) -> Dict[str, str]:
        """
        List directory contents with optional detailed information
        
        Args:
            path: Directory path to list
            detailed: Whether to include detailed file information
            
        Returns:
            Dict with status, message, and directory contents
        """
        try:
            dir_path = Path(path)
            
            if not dir_path.exists():
                return {
                    'status': 'error',
                    'message': f"❌ Directory not found: {path}",
                    'details': {'error_type': 'DirectoryNotFoundError'}
                }
            
            if not dir_path.is_dir():
                return {
                    'status': 'error',
                    'message': f"❌ Path is not a directory: {path}",
                    'details': {'error_type': 'NotADirectoryError'}
                }
            
            items = []
            total_size = 0
            dir_count = 0
            file_count = 0
            
            for item in sorted(dir_path.iterdir()):
                if item.is_dir():
                    dir_count += 1
                    if detailed:
                        try:
                            sub_items = len(list(item.iterdir()))
                            items.append(f"📁 {item.name}/ ({sub_items} items)")
                        except PermissionError:
                            items.append(f"📁 {item.name}/ (access denied)")
                    else:
                        items.append(f"📁 {item.name}/")
                else:
                    file_count += 1
                    try:
                        file_size = item.stat().st_size
                        total_size += file_size
                        if detailed:
                            modified = datetime.datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                            size_str = self._format_file_size(file_size)
                            items.append(f"📄 {item.name} ({size_str}, {modified})")
                        else:
                            items.append(f"📄 {item.name}")
                    except (PermissionError, OSError):
                        items.append(f"📄 {item.name} (access denied)")
            
            if not items:
                content = f"📂 Directory {path} is empty"
            else:
                content = f"📂 Contents of {path}:\n" + "\n".join(items)
                if detailed:
                    content += f"\n\n📊 Summary: {dir_count} directories, {file_count} files"
                    content += f"\n💾 Total size: {self._format_file_size(total_size)}"
            
            return {
                'status': 'success',
                'message': content,
                'details': {
                    'path': str(dir_path.absolute()),
                    'total_items': len(items),
                    'directories': dir_count,
                    'files': file_count,
                    'total_size': total_size
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f"❌ Error listing directory: {str(e)}",
                'details': {'error_type': type(e).__name__}
            }
    
    def create_directory(self, path: str) -> Dict[str, str]:
        """
        Create a directory (including parent directories)
        
        Args:
            path: Directory path to create
            
        Returns:
            Dict with status and message
        """
        try:
            dir_path = Path(path)
            
            if dir_path.exists():
                return {
                    'status': 'warning',
                    'message': f"⚠️ Directory already exists: {path}",
                    'details': {'already_exists': True}
                }
            
            dir_path.mkdir(parents=True, exist_ok=True)
            
            return {
                'status': 'success',
                'message': f"✅ Directory created successfully: {path}",
                'details': {
                    'path': str(dir_path.absolute()),
                    'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f"❌ Error creating directory: {str(e)}",
                'details': {'error_type': type(e).__name__}
            }
    
    def organize_files(self, path: str = ".") -> Dict[str, str]:
        """
        Organize files in a directory by type
        
        Args:
            path: Directory path to organize
            
        Returns:
            Dict with status and organization results
        """
        try:
            dir_path = Path(path)
            
            if not dir_path.exists() or not dir_path.is_dir():
                return {
                    'status': 'error',
                    'message': f"❌ Directory not found: {path}",
                    'details': {'error_type': 'DirectoryNotFoundError'}
                }
            
            organized_count = 0
            organization_log = []
            
            # Create organization folders
            for folder_name in self.file_type_mappings.keys():
                folder_path = dir_path / folder_name
                folder_path.mkdir(exist_ok=True)
            
            # Organize files
            for item in dir_path.iterdir():
                if item.is_file():
                    file_ext = item.suffix.lower()
                    
                    # Find appropriate folder
                    target_folder = None
                    for folder, extensions in self.file_type_mappings.items():
                        if file_ext in extensions:
                            target_folder = folder
                            break
                    
                    if target_folder:
                        target_path = dir_path / target_folder / item.name
                        
                        # Avoid overwriting existing files
                        if not target_path.exists():
                            try:
                                shutil.move(str(item), str(target_path))
                                organized_count += 1
                                organization_log.append(f"Moved {item.name} to {target_folder}/")
                            except Exception as e:
                                organization_log.append(f"Failed to move {item.name}: {str(e)}")
            
            # Clean up empty folders
            for folder_name in self.file_type_mappings.keys():
                folder_path = dir_path / folder_name
                if folder_path.exists() and not any(folder_path.iterdir()):
                    folder_path.rmdir()
            
            result_message = f"✅ Organized {organized_count} files in {path}"
            if organization_log:
                result_message += "\n\n📋 Organization Log:\n" + "\n".join(organization_log[:10])
                if len(organization_log) > 10:
                    result_message += f"\n... and {len(organization_log) - 10} more operations"
            
            return {
                'status': 'success',
                'message': result_message,
                'details': {
                    'organized_count': organized_count,
                    'total_operations': len(organization_log),
                    'organization_log': organization_log
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f"❌ Error organizing files: {str(e)}",
                'details': {'error_type': type(e).__name__}
            }
    
    def create_project_structure(self, name: str, project_type: str = "python") -> Dict[str, str]:
        """
        Create a complete project structure
        
        Args:
            name: Project name
            project_type: Type of project (python, web, java, etc.)
            
        Returns:
            Dict with status and project creation results
        """
        try:
            project_path = Path.cwd() / name
            
            if project_path.exists():
                return {
                    'status': 'error',
                    'message': f"❌ Project '{name}' already exists at {project_path}",
                    'details': {'already_exists': True}
                }
            
            # Create project directory
            project_path.mkdir(parents=True, exist_ok=True)
            
            created_files = []
            
            if project_type.lower() == "python":
                # Python project structure
                (project_path / "src").mkdir(exist_ok=True)
                (project_path / "tests").mkdir(exist_ok=True)
                (project_path / "docs").mkdir(exist_ok=True)
                
                # Create main.py
                main_content = f'''#!/usr/bin/env python3
"""
{name} - Main Application
Created by JARVIS-X
"""

def main():
    """Main application entry point"""
    print(f"Welcome to {name}!")
    print("This is your main application.")

if __name__ == "__main__":
    main()
'''
                with open(project_path / "main.py", "w", encoding='utf-8') as f:
                    f.write(main_content)
                created_files.append("main.py")
                
                # Create requirements.txt
                requirements_content = """# Python Dependencies
# Add your project dependencies here
# Example:
# requests>=2.25.0
# numpy>=1.20.0
"""
                with open(project_path / "requirements.txt", "w", encoding='utf-8') as f:
                    f.write(requirements_content)
                created_files.append("requirements.txt")
                
                # Create README.md
                readme_content = f"""# {name}

## Description
This project was created by JARVIS-X AI Assistant.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py
```

## Project Structure
```
{name}/
├── main.py          # Main application file
├── requirements.txt # Python dependencies
├── README.md        # This file
├── src/            # Source code directory
├── tests/          # Test files directory
└── docs/           # Documentation directory
```

## Development
- Created: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- Generator: JARVIS-X AI Assistant
"""
                with open(project_path / "README.md", "w", encoding='utf-8') as f:
                    f.write(readme_content)
                created_files.append("README.md")
                
            elif project_type.lower() == "web":
                # Web project structure
                (project_path / "css").mkdir(exist_ok=True)
                (project_path / "js").mkdir(exist_ok=True)
                (project_path / "images").mkdir(exist_ok=True)
                
                # Create index.html
                html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <h1>Welcome to {name}</h1>
        <p>Created by JARVIS-X AI Assistant</p>
    </header>
    
    <main>
        <section>
            <h2>About This Project</h2>
            <p>This is a web project structure created by JARVIS-X.</p>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2025 {name}. Generated by JARVIS-X.</p>
    </footer>
    
    <script src="js/script.js"></script>
</body>
</html>'''
                with open(project_path / "index.html", "w") as f:
                    f.write(html_content)
                created_files.append("index.html")
                
                # Create CSS file
                css_content = f'''/* {name} - Stylesheet */
/* Generated by JARVIS-X AI Assistant */

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f4f4f4;
}}

header {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    padding: 2rem 0;
}}

header h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

main {{
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
}}

section {{
    background: white;
    padding: 2rem;
    margin-bottom: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}}

footer {{
    background: #333;
    color: white;
    text-align: center;
    padding: 1rem 0;
    margin-top: 2rem;
}}
'''
                with open(project_path / "css" / "style.css", "w") as f:
                    f.write(css_content)
                created_files.append("css/style.css")
                
                # Create JavaScript file
                js_content = f'''// {name} - JavaScript
// Generated by JARVIS-X AI Assistant

document.addEventListener('DOMContentLoaded', function() {{
    console.log('{name} loaded successfully!');
    console.log('Generated by JARVIS-X AI Assistant');
    
    // Add your JavaScript code here
}});

// Example function
function greetUser() {{
    alert('Hello from {name}!');
}}
'''
                with open(project_path / "js" / "script.js", "w") as f:
                    f.write(js_content)
                created_files.append("js/script.js")
            
            return {
                'status': 'success',
                'message': f"✅ Project '{name}' created successfully at {project_path}",
                'details': {
                    'project_path': str(project_path.absolute()),
                    'project_type': project_type,
                    'files_created': created_files,
                    'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f"❌ Error creating project: {str(e)}",
                'details': {'error_type': type(e).__name__}
            }
    
    def get_file_info(self, filepath: str) -> Dict[str, str]:
        """
        Get detailed information about a file
        
        Args:
            filepath: Path to the file
            
        Returns:
            Dict with file information
        """
        try:
            file_path = Path(filepath)
            
            if not file_path.exists():
                return {
                    'status': 'error',
                    'message': f"❌ File not found: {filepath}",
                    'details': {'error_type': 'FileNotFoundError'}
                }
            
            stat = file_path.stat()
            
            # Get file hash
            file_hash = self._get_file_hash(file_path)
            
            # Get MIME type
            mime_type, encoding = mimetypes.guess_type(filepath)
            
            info = {
                'path': str(file_path.absolute()),
                'name': file_path.name,
                'extension': file_path.suffix,
                'size': self._format_file_size(stat.st_size),
                'size_bytes': stat.st_size,
                'created': datetime.datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                'modified': datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                'accessed': datetime.datetime.fromtimestamp(stat.st_atime).strftime("%Y-%m-%d %H:%M:%S"),
                'mime_type': mime_type or 'unknown',
                'encoding': encoding or 'unknown',
                'hash_md5': file_hash,
                'is_directory': file_path.is_dir(),
                'is_file': file_path.is_file(),
                'permissions': oct(stat.st_mode)[-3:]
            }
            
            message = f"📋 File Information for {filepath}:\n"
            message += f"📄 Name: {info['name']}\n"
            message += f"📏 Size: {info['size']} ({info['size_bytes']} bytes)\n"
            message += f"📅 Created: {info['created']}\n"
            message += f"📅 Modified: {info['modified']}\n"
            message += f"🔧 MIME Type: {info['mime_type']}\n"
            message += f"🔐 Permissions: {info['permissions']}\n"
            message += f"🔑 MD5 Hash: {info['hash_md5']}"
            
            return {
                'status': 'success',
                'message': message,
                'details': info
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f"❌ Error getting file info: {str(e)}",
                'details': {'error_type': type(e).__name__}
            }
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Get MD5 hash of a file"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return "unknown"

# Singleton instance for global access
_file_operations_instance = None

def get_file_operations_manager():
    """Get singleton instance of FileOperationsManager"""
    global _file_operations_instance
    
    if _file_operations_instance is None:
        _file_operations_instance = FileOperationsManager()
    
    return _file_operations_instance
