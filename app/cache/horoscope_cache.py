"""
Author: nikhil.anand
Created at: 19/07/25
"""

from datetime import date
from typing import Dict, Optional, Any
from collections import OrderedDict
import threading


class HoroscopeCache:
    """
    Thread-safe singleton cache for storing personalized horoscope data.

    This class implements a singleton pattern with thread-safe operations for
    caching personalized horoscope content. It uses an LRU (Least Recently Used)
    eviction policy and automatically manages stale entries based on date.

    Features:
        - Singleton pattern ensures single cache instance across the application
        - Thread-safe operations using locks
        - LRU eviction policy for memory management
        - Automatic stale entry detection and cleanup
        - Date-based cache validation

    Attributes:
        _instance (Optional[HoroscopeCache]): Singleton instance
        _lock (threading.Lock): Class-level lock for singleton creation
        max_size (int): Maximum number of cache entries
        cache (OrderedDict): Ordered dictionary storing cache entries
        _cache_lock (threading.Lock): Instance-level lock for cache operations
        _initialized (bool): Flag to prevent re-initialization
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, max_size: int = 100) -> "HoroscopeCache":
        """
        Create or return the singleton instance of HoroscopeCache.

        This method implements the singleton pattern with thread safety,
        ensuring only one instance of the cache exists throughout the application.

        Args:
            max_size (int, optional): Maximum cache size. Defaults to 100.
                Only used during first instantiation.

        Returns:
            HoroscopeCache: The singleton cache instance
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, max_size: int = 100) -> None:
        """
        Initialize the cache with specified maximum size.

        This method initializes the cache only once due to the singleton pattern.
        Subsequent calls to __init__ will not re-initialize the cache.

        Args:
            max_size (int, optional): Maximum number of entries to store. Defaults to 100.
        """
        if not self._initialized:
            self.max_size = max_size
            self.cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
            self._cache_lock = threading.Lock()  # For thread-safe cache operations
            self._initialized = True

    @staticmethod
    def _generate_key(birth_date: str, name: str, language: str) -> str:
        """
        Generate a unique cache key from user information.

        This method creates a standardized cache key by combining birth date,
        name, and language. Names and languages are normalized to lowercase
        for consistent key generation.

        Args:
            birth_date (str): User's birth date
            name (str): User's name
            language (str): Response language

        Returns:
            str: Unique cache key in format "birth_date_name_language"

        Example:
            >>> HoroscopeCache._generate_key("1995-01-15", "John Doe", "ENGLISH")
            "1995-01-15_john doe_english"
        """
        return f"{birth_date}_{name.lower()}_{language.lower()}"

    def get(self, birth_date: str, name: str, language: str) -> Optional[str]:
        """
        Retrieve cached horoscope if it exists and is current.

        This method attempts to retrieve a cached horoscope for the given user
        information. It validates that the cached entry is from today and
        automatically removes stale entries. Uses LRU ordering by moving
        accessed items to the end.

        Args:
            birth_date (str): User's birth date
            name (str): User's name
            language (str): Response language

        Returns:
            Optional[str]: Cached horoscope text if found and current, None otherwise

        Example:
            >>> cache = HoroscopeCache()
            >>> horoscope = cache.get("1995-01-15", "John", "english")
            >>> print(horoscope)  # Returns cached text or None
        """
        key = self._generate_key(birth_date, name, language)

        with self._cache_lock:
            if key not in self.cache:
                return None

            cached_entry = self.cache[key]
            today = date.today().isoformat()

            # Check if cache is from today
            if cached_entry["date"] != today:
                # Remove stale entry
                del self.cache[key]
                return None

            # Move to end (LRU)
            self.cache.move_to_end(key)
            return cached_entry["horoscope"]

    def put(self, birth_date: str, name: str, language: str, horoscope: str) -> None:
        """
        Store a horoscope in the cache with today's date.

        This method stores a personalized horoscope in the cache with the current
        date. It prevents duplicate entries for the same user on the same day
        and implements LRU eviction when the cache exceeds its maximum size.

        Args:
            birth_date (str): User's birth date
            name (str): User's name
            language (str): Response language
            horoscope (str): Personalized horoscope text to cache

        Example:
            >>> cache = HoroscopeCache()
            >>> cache.put("1995-01-15", "John", "english", "Your horoscope for today...")
        """
        key = self._generate_key(birth_date, name, language)
        today = date.today().isoformat()

        with self._cache_lock:
            # If same date entry exists, don't add again
            if key in self.cache and self.cache[key]["date"] == today:
                return

            # Add new entry
            self.cache[key] = {"horoscope": horoscope, "date": today}

            # Move to end
            self.cache.move_to_end(key)

            # Remove oldest if size limit exceeded
            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False)

    def clear_stale_entries(self) -> int:
        """
        Remove all cache entries that are not from today.

        This method performs cache maintenance by removing all entries that
        are not from the current date. It's typically called as a scheduled
        task to prevent memory bloat from outdated horoscope data.

        Returns:
            int: Number of stale entries that were removed

        Example:
            >>> cache = HoroscopeCache()
            >>> removed_count = cache.clear_stale_entries()
            >>> print(f"Removed {removed_count} stale entries")
        """
        today = date.today().isoformat()

        with self._cache_lock:
            stale_keys = []

            for key, entry in self.cache.items():
                if entry["date"] != today:
                    stale_keys.append(key)

            for key in stale_keys:
                del self.cache[key]

            return len(stale_keys)
