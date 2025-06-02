from models.command_log import CommandLog
from typing import Optional, List, Dict, Any
import datetime
from peewee import fn


def log_command(
    server_id: Optional[str], 
    server_name: Optional[str], 
    user_id: str, 
    user_name: str, 
    command_name: str
) -> CommandLog:
    """
    Log a command execution to the database
    
    Args:
        server_id: ID of the server where the command was executed (None for DMs)
        server_name: Name of the server where the command was executed (None for DMs)
        user_id: ID of the user who executed the command
        user_name: Name of the user who executed the command
        command_name: Name of the command that was executed
        
    Returns:
        The created CommandLog entry
    """
    command_log = CommandLog(
        server_id=server_id,
        server_name=server_name,
        user_id=user_id,
        user_name=user_name,
        command_name=command_name
    )
    command_log.save()
    return command_log


def get_top_commands(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get the most used commands across all servers
    
    Args:
        limit: Maximum number of commands to return
        
    Returns:
        List of dicts with command_name and count keys
    """
    query = (CommandLog
             .select(CommandLog.command_name, fn.COUNT(CommandLog.id).alias('count'))
             .group_by(CommandLog.command_name)
             .order_by(fn.COUNT(CommandLog.id).desc())
             .limit(limit))
    
    return [{'command_name': row.command_name, 'count': row.count} for row in query]


def get_top_servers(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get the servers with the most command usage
    
    Args:
        limit: Maximum number of servers to return
        
    Returns:
        List of dicts with server_id, server_name and count keys
    """
    query = (CommandLog
             .select(CommandLog.server_id, CommandLog.server_name, fn.COUNT(CommandLog.id).alias('count'))
             .where(CommandLog.server_id.is_null(False))
             .group_by(CommandLog.server_id)
             .order_by(fn.COUNT(CommandLog.id).desc())
             .limit(limit))
    
    return [{'server_id': row.server_id, 'server_name': row.server_name, 'count': row.count} for row in query]


def get_top_users(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get the users with the most command usage across all servers
    
    Args:
        limit: Maximum number of users to return
        
    Returns:
        List of dicts with user_id, user_name and count keys
    """
    query = (CommandLog
             .select(CommandLog.user_id, CommandLog.user_name, fn.COUNT(CommandLog.id).alias('count'))
             .group_by(CommandLog.user_id)
             .order_by(fn.COUNT(CommandLog.id).desc())
             .limit(limit))
    
    return [{'user_id': row.user_id, 'user_name': row.user_name, 'count': row.count} for row in query]


def get_top_commands_by_server(server_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get the most used commands for a specific server
    
    Args:
        server_id: ID of the server to get commands for
        limit: Maximum number of commands to return
        
    Returns:
        List of dicts with command_name and count keys
    """
    query = (CommandLog
             .select(CommandLog.command_name, fn.COUNT(CommandLog.id).alias('count'))
             .where(CommandLog.server_id == server_id)
             .group_by(CommandLog.command_name)
             .order_by(fn.COUNT(CommandLog.id).desc())
             .limit(limit))
    
    return [{'command_name': row.command_name, 'count': row.count} for row in query]


def get_command_usage_over_time(days: int = 30) -> Dict[str, int]:
    """
    Get command usage counts per day for the past specified number of days
    
    Args:
        days: Number of days to look back
        
    Returns:
        Dictionary mapping dates to command counts
    """
    start_date = datetime.datetime.now() - datetime.timedelta(days=days)
    
    query = (CommandLog
             .select(fn.DATE(CommandLog.timestamp).alias('date'), 
                    fn.COUNT(CommandLog.id).alias('count'))
             .where(CommandLog.timestamp >= start_date)
             .group_by(fn.DATE(CommandLog.timestamp))
             .order_by(fn.DATE(CommandLog.timestamp)))
    
    return {str(row.date): row.count for row in query}