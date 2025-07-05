"""
Cloud Integration API Endpoints for GhostLAN SimWorld
FastAPI endpoints for cloud deployment and management
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import logging

from cloud_integration.cloud_services import CloudIntegrationManager, CloudConfig

logger = logging.getLogger(__name__)

# Pydantic models
class CloudProviderConfig(BaseModel):
    provider: str  # 'aws', 'azure', 'gcp'
    region: str
    credentials: Dict[str, Any]
    auto_scaling: bool = True
    load_balancing: bool = True
    monitoring: bool = True

class ApplicationDeployConfig(BaseModel):
    name: str
    image: str
    port: int = 8000
    cpu: str = "256"
    memory: str = "512"
    replicas: int = 2
    environment: Dict[str, str] = {}

class LoadBalancerConfig(BaseModel):
    name: str
    port: int = 8000
    protocol: str = "HTTP"
    health_check_path: str = "/health"
    vpc_id: Optional[str] = None
    subnets: List[str] = []
    security_groups: List[str] = []

class AutoScalingConfig(BaseModel):
    group_name: str
    min_size: int = 1
    max_size: int = 10
    desired_capacity: int = 2
    cpu_threshold_high: float = 80.0
    cpu_threshold_low: float = 20.0

class MonitoringConfig(BaseModel):
    app_name: str
    region: str = "us-east-1"
    alert_email: str = "admin@ghostlan.com"
    cpu_threshold: float = 90.0
    memory_threshold: float = 85.0

# Router
cloud_router = APIRouter(prefix="/cloud", tags=["Cloud Integration"])

# Dependency to get cloud manager
def get_cloud_manager() -> CloudIntegrationManager:
    # This would be injected from the main app
    from main import cloud_manager
    return cloud_manager

@cloud_router.post("/providers")
async def add_cloud_provider(
    config: CloudProviderConfig,
    cloud_manager: CloudIntegrationManager = Depends(get_cloud_manager)
):
    """Add cloud provider"""
    try:
        cloud_config = CloudConfig(
            provider=config.provider,
            region=config.region,
            credentials=config.credentials,
            auto_scaling=config.auto_scaling,
            load_balancing=config.load_balancing,
            monitoring=config.monitoring
        )
        
        await cloud_manager.add_cloud_provider(config.provider, cloud_config)
        
        return {
            "success": True,
            "message": f"Cloud provider {config.provider} added successfully",
            "provider": config.provider,
            "region": config.region
        }
        
    except Exception as e:
        logger.error(f"Failed to add cloud provider: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@cloud_router.post("/deploy")
async def deploy_application(
    provider: str,
    config: ApplicationDeployConfig,
    cloud_manager: CloudIntegrationManager = Depends(get_cloud_manager)
):
    """Deploy application to cloud"""
    try:
        deploy_config = {
            'image': config.image,
            'port': config.port,
            'cpu': config.cpu,
            'memory': config.memory,
            'replicas': config.replicas,
            'environment': config.environment
        }
        
        result = await cloud_manager.deploy_application(provider, config.name, deploy_config)
        
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
            
        return {
            "success": True,
            "message": f"Application {config.name} deployed successfully",
            "provider": provider,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Failed to deploy application: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@cloud_router.post("/load-balancer")
async def setup_load_balancer(
    provider: str,
    config: LoadBalancerConfig,
    cloud_manager: CloudIntegrationManager = Depends(get_cloud_manager)
):
    """Setup load balancer"""
    try:
        lb_config = {
            'port': config.port,
            'protocol': config.protocol,
            'health_check_path': config.health_check_path,
            'vpc_id': config.vpc_id,
            'subnets': config.subnets,
            'security_groups': config.security_groups
        }
        
        result = await cloud_manager.setup_load_balancing(provider, config.name, lb_config)
        
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
            
        return {
            "success": True,
            "message": f"Load balancer {config.name} setup successfully",
            "provider": provider,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Failed to setup load balancer: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@cloud_router.post("/auto-scaling")
async def setup_auto_scaling(
    provider: str,
    config: AutoScalingConfig,
    cloud_manager: CloudIntegrationManager = Depends(get_cloud_manager)
):
    """Setup auto scaling"""
    try:
        scaling_config = {
            'min_size': config.min_size,
            'max_size': config.max_size,
            'desired_capacity': config.desired_capacity,
            'cpu_threshold_high': config.cpu_threshold_high,
            'cpu_threshold_low': config.cpu_threshold_low
        }
        
        result = await cloud_manager.setup_auto_scaling(provider, config.group_name, scaling_config)
        
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
            
        return {
            "success": True,
            "message": f"Auto scaling {config.group_name} setup successfully",
            "provider": provider,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Failed to setup auto scaling: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@cloud_router.post("/monitoring")
async def setup_monitoring(
    provider: str,
    config: MonitoringConfig,
    cloud_manager: CloudIntegrationManager = Depends(get_cloud_manager)
):
    """Setup monitoring"""
    try:
        monitoring_config = {
            'region': config.region,
            'alert_email': config.alert_email,
            'cpu_threshold': config.cpu_threshold,
            'memory_threshold': config.memory_threshold
        }
        
        result = await cloud_manager.setup_monitoring(provider, config.app_name, monitoring_config)
        
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
            
        return {
            "success": True,
            "message": f"Monitoring for {config.app_name} setup successfully",
            "provider": provider,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Failed to setup monitoring: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@cloud_router.get("/status/{provider}")
async def get_cloud_status(
    provider: str,
    cloud_manager: CloudIntegrationManager = Depends(get_cloud_manager)
):
    """Get cloud provider status"""
    try:
        status = await cloud_manager.get_cloud_status(provider)
        
        if 'error' in status:
            raise HTTPException(status_code=404, detail=status['error'])
            
        return status
        
    except Exception as e:
        logger.error(f"Failed to get cloud status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@cloud_router.get("/providers")
async def list_cloud_providers(
    cloud_manager: CloudIntegrationManager = Depends(get_cloud_manager)
):
    """List configured cloud providers"""
    try:
        providers = list(cloud_manager.cloud_services.keys())
        
        return {
            "providers": providers,
            "count": len(providers)
        }
        
    except Exception as e:
        logger.error(f"Failed to list cloud providers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@cloud_router.delete("/providers/{provider}")
async def remove_cloud_provider(
    provider: str,
    cloud_manager: CloudIntegrationManager = Depends(get_cloud_manager)
):
    """Remove cloud provider"""
    try:
        if provider in cloud_manager.cloud_services:
            del cloud_manager.cloud_services[provider]
            del cloud_manager.load_balancers[provider]
            del cloud_manager.auto_scaling[provider]
            del cloud_manager.monitoring[provider]
            
            return {
                "success": True,
                "message": f"Cloud provider {provider} removed successfully"
            }
        else:
            raise HTTPException(status_code=404, detail=f"Provider {provider} not found")
            
    except Exception as e:
        logger.error(f"Failed to remove cloud provider: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@cloud_router.post("/scale/{provider}/{group_name}")
async def scale_group(
    provider: str,
    group_name: str,
    action: str,  # 'up' or 'down'
    instances: int = 1,
    cloud_manager: CloudIntegrationManager = Depends(get_cloud_manager)
):
    """Manually scale auto-scaling group"""
    try:
        if provider not in cloud_manager.auto_scaling:
            raise HTTPException(status_code=404, detail=f"Provider {provider} not found")
            
        auto_scaling = cloud_manager.auto_scaling[provider]
        
        if action == 'up':
            await auto_scaling.scale_up(group_name, instances)
        elif action == 'down':
            await auto_scaling.scale_down(group_name, instances)
        else:
            raise HTTPException(status_code=400, detail="Action must be 'up' or 'down'")
            
        return {
            "success": True,
            "message": f"Scaled {group_name} {action} by {instances} instances",
            "provider": provider,
            "group_name": group_name,
            "action": action,
            "instances": instances
        }
        
    except Exception as e:
        logger.error(f"Failed to scale group: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@cloud_router.get("/metrics/{provider}")
async def get_cloud_metrics(
    provider: str,
    namespace: str,
    metric_name: str,
    cloud_manager: CloudIntegrationManager = Depends(get_cloud_manager)
):
    """Get cloud metrics"""
    try:
        if provider not in cloud_manager.monitoring:
            raise HTTPException(status_code=404, detail=f"Provider {provider} not found")
            
        monitoring = cloud_manager.monitoring[provider]
        
        # Simplified dimensions - in production would be more flexible
        dimensions = [{'Name': 'ServiceName', 'Value': 'GhostLAN'}]
        
        metrics = await monitoring.get_metrics(namespace, metric_name, dimensions)
        
        if 'error' in metrics:
            raise HTTPException(status_code=400, detail=metrics['error'])
            
        return {
            "provider": provider,
            "namespace": namespace,
            "metric_name": metric_name,
            "metrics": metrics
        }
        
    except Exception as e:
        logger.error(f"Failed to get cloud metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@cloud_router.get("/health")
async def cloud_health_check():
    """Health check for cloud integration"""
    return {
        "status": "healthy",
        "service": "cloud-integration",
        "timestamp": "2024-01-01T00:00:00Z"
    } 