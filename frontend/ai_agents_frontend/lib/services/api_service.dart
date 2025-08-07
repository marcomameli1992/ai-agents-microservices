import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/search_result.dart';

class ApiService {
  // In produzione, potresti voler configurare questo URL
  static const String baseUrl = 'http://localhost:8000';

  Future<List<SearchResult>> search(String query) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/search?query=$query'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List<dynamic> results = data['results'] ?? [];
        return results.map((json) => SearchResult.fromJson(json)).toList();
      } else {
        throw Exception(
          'Failed to load search results: ${response.statusCode}',
        );
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }

  Future<Map<String, dynamic>> analyze(String query) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/analyze'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'query': query}),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to analyze content: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }
}
