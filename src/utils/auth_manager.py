# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime, timedelta


class AuthManager:
    def __init__(self, config_file="user_config.json"):
        self.config_file = config_file
        self.config_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.config_dir, self.config_file)

    def save_login_info(self, username, remember_me=False, real_name=None):
        """保存登录信息到JSON文件"""
        try:
            config_data = self._load_config()

            if remember_me:
                # 保存登录信息
                config_data["login_info"] = {
                    "username": username,
                    "real_name": real_name or username,  # 保存真实姓名，如果没有则使用账号ID
                    "remember_me": True,
                    "last_login": datetime.now().isoformat()
                }
            else:
                # 如果不记住登录，清除之前的登录信息
                if "login_info" in config_data:
                    del config_data["login_info"]

            self._save_config(config_data)
            return True
        except Exception as e:
            print(f"保存登录信息失败: {e}")
            return False

    def get_saved_login_info(self):
        """获取保存的登录信息"""
        try:
            config_data = self._load_config()

            if "login_info" in config_data:
                login_info = config_data["login_info"]
                # 检查是否设置了记住登录
                if login_info.get("remember_me", False):
                    # 可以添加时间检查逻辑（例如30天内有效）
                    last_login_str = login_info.get("last_login", "")
                    if last_login_str:
                        try:
                            last_login = datetime.fromisoformat(last_login_str)
                            # 检查是否在30天内
                            if datetime.now() - last_login <= timedelta(days=30):
                                return {
                                    "username": login_info.get("username", ""),
                                    "real_name": login_info.get("real_name", login_info.get("username", "")),
                                    "remember_me": True
                                }
                        except ValueError:
                            pass
                    else:
                        return {
                            "username": login_info.get("username", ""),
                            "real_name": login_info.get("real_name", login_info.get("username", "")),
                            "remember_me": True
                        }

            return {"username": "", "real_name": "", "remember_me": False}
        except Exception as e:
            print(f"获取登录信息失败: {e}")
            return {"username": "", "real_name": "", "remember_me": False}

    def clear_login_info(self):
        """清除保存的登录信息"""
        try:
            config_data = self._load_config()
            if "login_info" in config_data:
                del config_data["login_info"]
            self._save_config(config_data)
            return True
        except Exception as e:
            print(f"清除登录信息失败: {e}")
            return False

    def _load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, Exception):
                return {}
        return {}

    def _save_config(self, config_data):
        """保存配置文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            raise