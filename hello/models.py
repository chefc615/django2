from django.db import models

class Recipe(models.Model):
    recipe_id = models.CharField(max_length=255, primary_key=True)
    title = models.TextField(blank=True, null=True)
    canonical_url = models.TextField(blank=True, null=True)
    total_time = models.IntegerField(blank=True, null=True)
    yields = models.TextField(blank=True, null=True)
    nutrients = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    ingredients = models.TextField(blank=True, null=True)
    ingredient_groups = models.TextField(blank=True, null=True)
    instructions_list = models.TextField(blank=True, null=True)
    equipment = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'recipe_table'  # Specifies the actual database table name
        ordering = ['recipe_id']

    def __str__(self):
        return self.title or self.recipe_id

class RecipeIngredient(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        db_column='recipe_id'  # References the 'recipe_id' column in 'recipe_ingredient_table'
    )
    type = models.TextField(blank=True, null=True)
    grams = models.FloatField(blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)
    metric_measurement = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'recipe_ingredient_table'  # Specifies the actual database table name

    def __str__(self):
        return f"{self.qty} {self.unit} {self.type} for {self.recipe.title}"
