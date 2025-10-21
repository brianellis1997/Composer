# Compute Requirements and M1 Pro Capabilities

## Hardware Specifications

### MacBook M1 Pro
- **Chip**: Apple M1 Pro
- **CPU Cores**: 10 (8 performance + 2 efficiency)
- **GPU**: Integrated (16-core GPU in M1 Pro)
- **Memory**: 16 GB unified RAM
- **Storage**: SSD (fast I/O)

### PyTorch MPS Support
- **Device**: `torch.device("mps")` - Metal Performance Shaders
- **PyTorch Version**: 2.9.0
- **MPS Status**: Available and built-in
- **Requirements**: macOS 12.3+

## Capability Assessment

### Training Workloads

#### Small Models (Feasible on M1 Pro)
- **Model Size**: Up to 100M parameters
- **Batch Size**: 2-4 sequences
- **Sequence Length**: 1024-2048 tokens
- **Training Time**: Days to weeks for small datasets
- **Example**: Fine-tuning SkyTNT MIDI model on single composer

**Verdict**: ✅ Suitable for crawl and walk stages

#### Medium Models (Marginal)
- **Model Size**: 100M-350M parameters
- **Batch Size**: 1-2 sequences
- **Sequence Length**: 512-1024 tokens
- **Training Time**: Weeks to months
- **Memory Pressure**: High, may require gradient checkpointing

**Verdict**: ⚠️ Possible but slow, may need optimizations

#### Large Models (Not Recommended)
- **Model Size**: >350M parameters
- **Memory**: Exceeds 16GB RAM capacity
- **Training Time**: Prohibitively slow

**Verdict**: ❌ Requires cloud compute (A100, H100, etc.)

### Inference Workloads

#### Generation Speed (Estimated)
- **Small Model**: ~10-50 tokens/second
- **Medium Model**: ~5-20 tokens/second
- **Long Sequences**: 1-2 minute generation for 2000 tokens

**Verdict**: ✅ Acceptable for development and testing

### Memory Limitations

#### Available Memory Budget
- **System**: ~16 GB total
- **Reserved for OS**: ~2-3 GB
- **Available for PyTorch**: ~13 GB

#### Memory Usage Breakdown (Example: 100M model)
- **Model Weights**: ~400 MB (fp32) or ~200 MB (fp16)
- **Optimizer States**: ~800 MB (Adam)
- **Gradients**: ~400 MB
- **Activations**: ~2-6 GB (depends on batch size and sequence length)
- **CUDA/MPS Context**: ~1-2 GB

**Total**: ~4-10 GB (comfortably within budget)

### Optimization Strategies for M1 Pro

#### 1. Mixed Precision Training
```python
from torch.cuda.amp import autocast, GradScaler
# Use fp16 for forward/backward, fp32 for optimization
```
**Benefit**: 40-50% memory reduction, faster computation

#### 2. Gradient Accumulation
```python
# Simulate larger batch size
accumulation_steps = 8
effective_batch_size = batch_size * accumulation_steps
```
**Benefit**: Larger effective batch sizes without OOM

#### 3. Gradient Checkpointing
```python
# Trade computation for memory
model.gradient_checkpointing_enable()
```
**Benefit**: 2-3x memory reduction for activations

#### 4. Smaller Sequence Lengths
- Chunk long compositions into 512-1024 token segments
- Use sliding window during generation
- Overlap segments for continuity

#### 5. LoRA Fine-tuning
- Only train low-rank adapter matrices
- Keep pre-trained weights frozen
- **Memory**: 90%+ reduction in trainable parameters

**Recommended for M1 Pro**: LoRA is ideal for limited compute

### MPS-Specific Considerations

#### Known Issues
- Some PyTorch operations not implemented in MPS
- Solution: Set `PYTORCH_ENABLE_MPS_FALLBACK=1` to use CPU fallback

#### Performance Tips
1. Keep data on MPS device (minimize transfers)
2. Use contiguous tensors when possible
3. Profile with `torch.profiler` to identify bottlenecks

#### Compatibility
- Most transformer operations are supported
- Attention mechanisms work well on MPS
- Some custom operations may fall back to CPU

## Cloud Compute Recommendations

### When to Move to Cloud
1. **Model Size**: > 200M parameters
2. **Dataset Size**: > 100k sequences
3. **Training Time**: > 2 weeks estimated on M1
4. **Experimentation**: Need for rapid iteration

### Recommended Platforms

#### Google Colab
- **Tier**: Free / Pro ($10/month)
- **GPU**: T4 (free), V100/A100 (Pro)
- **Memory**: 12-40 GB GPU RAM
- **Pros**: Easy setup, Jupyter notebooks
- **Cons**: Session timeouts, limited persistent storage

#### AWS SageMaker / EC2
- **Instance**: ml.g4dn.xlarge (T4), ml.p3.2xlarge (V100)
- **Cost**: $0.50-3/hour
- **Pros**: Scalable, persistent storage
- **Cons**: More setup required, cost management

#### Lambda Labs
- **GPU**: RTX 4090, A100, H100
- **Cost**: $0.50-2/hour
- **Pros**: GPU-focused, good value
- **Cons**: Availability varies

### Estimated Costs (Example)

#### Scenario: Fine-tune 100M parameter model on Bach dataset
- **M1 Pro**: Free, ~1-2 weeks training time
- **Colab Pro**: $10/month, ~2-3 days
- **AWS p3.2xlarge**: ~$100-150 total, ~1-2 days

## Recommendations by Project Phase

### Crawl Stage (Current)
**Hardware**: M1 Pro (local)
**Workload**:
- Small model inference testing
- Dataset exploration
- Preprocessing pipeline development
- Small-scale fine-tuning experiments (100-1000 samples)

**Verdict**: ✅ M1 Pro is perfect for this stage

### Walk Stage
**Hardware**: M1 Pro + optional cloud for experiments
**Workload**:
- Composer-specific fine-tuning (1k-10k samples)
- Hyperparameter tuning
- Evaluation and comparison
- LoRA adapters for multiple composers

**Recommendation**:
- Primary development on M1 Pro
- Cloud for final training runs if needed
- LoRA fine-tuning to stay within M1 Pro limits

### Run Stage
**Hardware**: Cloud compute (A100/H100)
**Workload**:
- Large-scale pre-training
- Full model training on complete datasets
- Production deployment
- Multi-composer multi-task learning

**Recommendation**: Budget $500-2000 for compute depending on scale

## Benchmarking Plan

### Baseline Tests on M1 Pro
1. Load SkyTNT model and measure memory usage
2. Generate 100 samples, measure time/token
3. Fine-tune on 1000 samples, measure epoch time
4. Identify memory bottlenecks
5. Test gradient accumulation and LoRA

### Success Criteria for M1 Pro
- ✅ Can load and run inference comfortably
- ✅ Fine-tuning converges in <1 week for single composer
- ✅ Generation quality is reasonable
- ✅ Memory usage <12 GB during training

If any criteria fail, move compute-heavy workloads to cloud.
